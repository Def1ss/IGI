"""
Purpose: Business logic for Variant 3 tasks
Lab: Laboratory Work 3
Version: 1.0
Developer: Daniil Vadimovich Borsuk
Date: 2026-03-30
"""

import math
import string

def task1_series(x: float, eps: float) -> tuple:
    """
    Calculates ln(1+x) using Maclaurin series up to a given precision eps.
    Condition: |x| < 1.
    """
    n = 1
    term = x
    series_sum = 0.0
    
    while abs(term) >= eps and n < 500:
        series_sum += term
        n += 1
        term = ((-1) ** (n - 1)) * (x**n) / n
        
    math_val = math.log(1 + x)
    return n - 1, series_sum, math_val

def task3_is_hex(text: str) -> bool:
    """
    Determines if the entered string is a valid hexadecimal number.
    """
    clean_text = text.strip()
    
    if clean_text.startswith('-') or clean_text.startswith('+'):
        clean_text = clean_text[1:]
        
    if clean_text.lower().startswith('0x'):
        clean_text = clean_text[2:]
        
    if not clean_text:
        return False
        
    hex_chars = set("0123456789abcdefABCDEF")
    for char in clean_text:
        if char not in hex_chars:
            return False
            
    return True

def task4_analyze_alice(text: str) -> tuple:
    """
    Analyzes the predefined Alice string.
    a) Number of words and list of words with even length
    c) Repeating words
    """
    
    raw_words = text.rsplit()
    clean_words = [w.strip(string.punctuation) for w in raw_words]
    clean_words = [w for w in clean_words if w]
    

    total_words = len(clean_words)
    even_len_words = [w for w in clean_words if len(w) % 2 == 0]
    
    a_words = [w for w in clean_words if w.lower().startswith('a')]
    shortest_a_word = min(a_words, key=len) if a_words else ""
    
    word_freq = {}
    for w in clean_words:
        w_lower = w.lower()
        word_freq[w_lower] = word_freq.get(w_lower, 0) + 1
        
    repeating_words = [w for w, count in word_freq.items() if count > 1]
    
    return total_words, even_len_words, shortest_a_word, repeating_words

def task5_process_list(lst: list) -> tuple:
    """
    Processes a list of floats.
    Returns max by absolute value and sum of elements before the last positive element.
    """
    if not lst:
        return None, 0.0
        
    max_mod_val = max(lst, key=abs)
    
    last_pos_idx = -1
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] > 0:
            last_pos_idx = i
            break
            
    sum_before = 0.0
    if last_pos_idx > 0:
        sum_before = sum(lst[:last_pos_idx])
        
    return max_mod_val, sum_before

    
    
# 5 and "" and 9.7 

# 5 or "" or 9.7

# (2, 5, 7) * 2