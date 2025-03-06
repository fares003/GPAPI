import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re
from torch.cuda.amp import autocast

# Cache models for reuse
model_cache = {}

def load_model(src_lang, tgt_lang):
    """
    Loads and caches the translation model to avoid repeated loading.
    """
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    
    if model_name in model_cache:
        return model_cache[model_name]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Loading model: {model_name} on {device}")

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        model_cache[model_name] = (tokenizer, model, device)
        return model_cache[model_name]
    except Exception as e:
        print(f"Model loading failed: {e}")
        return None

def split_text_into_sentences(text):
    """
    Splits long text into sentences while keeping context intact.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)  # Split based on punctuation
    return sentences

def translate_text(text, src_lang, tgt_lang, batch_size=8):
    """
    Translates long text efficiently by breaking it into smaller parts and using batching.
    """
    sentences = split_text_into_sentences(text)  # Split text into sentences

    result = load_model(src_lang, tgt_lang)
    if result is None:
        return "Translation not available"

    tokenizer, model, device = result

    translations = []
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i + batch_size]
        input_ids = tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512).input_ids.to(device)
        
        with torch.no_grad():
            with autocast():  # Use mixed precision if available
                output = model.generate(input_ids, max_length=512)  # Increase max length for translation
        
        translated_sentences = tokenizer.batch_decode(output, skip_special_tokens=True)
        translations.extend(translated_sentences)

    return " ".join(translations)  # Reassemble the translation