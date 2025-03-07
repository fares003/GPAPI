import torch
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

def text_summerization(text):
    model_name = "google/pegasus-large"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    # Move model to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Example text
    #text =sentences
    # Encode input text & move to GPU
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)

    # FAST GENERATION SETTINGS
    summary_ids = model.generate(
        **inputs, 
        max_length=100, min_length=20, 
        length_penalty=1.0,  
        num_beams=2,  
        early_stopping=True,  
        no_repeat_ngram_size=3,  
        do_sample=True,  
        top_k=50,  
        top_p=0.95  
    )

    # Decode & print summary
    summary3 = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary3