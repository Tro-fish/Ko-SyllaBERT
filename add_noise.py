import random
import unicodedata
from tqdm import tqdm
import argparse

# 두벌식 키보드 배열 정의 (영어 및 한글)

english_layout = [
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm'],
]
korean_layout = [
    ['ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅅ', 'ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ'],
    ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅎ', 'ㅗ', 'ㅓ', 'ㅏ', 'ㅣ'],
    ['ㅋ', 'ㅌ', 'ㅊ', 'ㅍ', 'ㅠ', 'ㅜ', 'ㅡ']
]

# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSEONG = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 중성 리스트. 00 ~ 20
JUNGSEONG = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSEONG = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

# 복합 자음 및 모음 분리 맵
COMPLEX_JONGSEONG_MAP = {
    'ㄳ': ['ㄱ', 'ㅅ'],
    'ㄵ': ['ㄴ', 'ㅈ'],
    'ㄶ': ['ㄴ', 'ㅎ'],
    'ㄺ': ['ㄹ', 'ㄱ'],
    'ㄻ': ['ㄹ', 'ㅁ'],
    'ㄼ': ['ㄹ', 'ㅂ'],
    'ㄽ': ['ㄹ', 'ㅅ'],
    'ㄾ': ['ㄹ', 'ㅌ'],
    'ㄿ': ['ㄹ', 'ㅍ'],
    'ㅀ': ['ㄹ', 'ㅎ'],
    'ㅄ': ['ㅂ', 'ㅅ']
}

COMPLEX_JUNGSEONG_MAP = {
    'ㅘ': ['ㅗ', 'ㅏ'],
    'ㅙ': ['ㅗ', 'ㅐ'],
    'ㅚ': ['ㅗ', 'ㅣ'],
    'ㅝ': ['ㅜ', 'ㅓ'],
    'ㅞ': ['ㅜ', 'ㅔ'],
    'ㅟ': ['ㅜ', 'ㅣ'],
    'ㅢ': ['ㅡ', 'ㅣ'],
    'ㅒ': ['ㅑ', 'ㅣ'],
    'ㅖ': ['ㅕ', 'ㅣ'],
}

# 주어진 문자의 위치를 찾는 함수
def find_char_position(char,lan):
    if lan == "english":
        keyboard_layout = english_layout
    else:
        keyboard_layout = korean_layout
    char = unicodedata.normalize('NFC', char)
    for row_idx, row in enumerate(keyboard_layout):
        for col_idx, col in enumerate(row):
            normalized_col = unicodedata.normalize('NFC', col)
            if char == normalized_col:
                return (row_idx, col_idx)
    return None

# 문자를 분해하여 재시도하는 함수
def find_char_position_with_fallback(char,lan):
    pos = find_char_position(char,lan)
    if pos is None:
        #print("complex pos: ",char)
        if char in COMPLEX_JONGSEONG_MAP:
            components = COMPLEX_JONGSEONG_MAP[char]
        elif char in COMPLEX_JUNGSEONG_MAP:
            components = COMPLEX_JUNGSEONG_MAP[char]
        else:
            # 복합 자음이 아닐 경우
            if char == 'ㅆ':
                components = ['ㅅ', 'ㅅ']
            elif char == 'ㅉ':
                components = ['ㅈ', 'ㅈ']
            elif char == 'ㄲ':
                components = ['ㄱ', 'ㄱ'] 
            elif char == 'ㄸ':
                components = ['ㄷ', 'ㄷ'] 
            elif char == 'ㅃ':
                components = ['ㅂ', 'ㅂ'] 
        fallback_char = random.choice(components)
        pos = find_char_position(fallback_char,lan)
    return pos

# 특정 위치의 주변 문자들을 반환하는 함수
def get_adjacent_chars(row, col, layout):
    adjacent_chars = []
    for i in range(max(0, row-1), min(len(layout), row+2)):
        for j in range(max(0, col-1), min(len(layout[i]), col+2)):
            if (i, j) != (row, col):
                adjacent_chars.append(layout[i][j])
    return adjacent_chars

# 한글 분해 함수
def decompose_hangul(char):
    if '가' <= char <= '힣':
        char_code = ord(char) - BASE_CODE
        chosung_index = int(char_code / CHOSUNG)
        jungsung_index = int((char_code - (CHOSUNG * chosung_index)) / JUNGSUNG)
        jongsung_index = int((char_code - (CHOSUNG * chosung_index) - (JUNGSUNG * jungsung_index)))

        chosung = CHOSEONG[chosung_index]
        jungsung = JUNGSEONG[jungsung_index]
        jongsung = JONGSEONG[jongsung_index] if jongsung_index != 0 else None
        
        return chosung, jungsung, jongsung
    elif char in COMPLEX_JUNGSEONG_MAP:
        return None, char, None
    elif char in COMPLEX_JONGSEONG_MAP:
        return None, None, char
    else:
        return char, None, None

# 한글 조합 함수
def compose_hangul(cho, jung='', jong=''):
    cho_index = CHOSEONG.index(cho)
    jung_index = JUNGSEONG.index(jung)
    jong_index = JONGSEONG.index(jong) if jong else 0
    
    hangul_char = chr(0xAC00 + (cho_index * 21 + jung_index) * 28 + jong_index)
    return hangul_char

# 한글과 영어 문자 여부 확인 함수
def is_korean_or_english(char):
    return ('가' <= char <= '힣') or ('A' <= char <= 'Z') or ('a' <= char <= 'z')

# 문장에 노이즈를 주는 함수
def add_noise_to_text(text, noise_percentage):
    noisy_text = list(text)
    # 한글, 영어에만 noise를 준다
    valid_indices = [idx for idx, char in enumerate(text) if is_korean_or_english(char)]
    num_noisy_chars = int(len(valid_indices) * noise_percentage)
    # 한글, 영어 중에서 noise가 들어갈 인덱스
    noisy_indices = random.sample(valid_indices, num_noisy_chars)

    for idx in noisy_indices:
        char = text[idx]
        # 영어 처리
        if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
            pos = find_char_position(char.lower(), "english")
            row, col = pos
            adjacent_chars = get_adjacent_chars(row, col, english_layout)
            new_char = random.choice([c for c in adjacent_chars if c.isalpha()])
            noisy_text[idx] = new_char.upper() if char.isupper() else new_char
        # 한글 처리
        if '가' <= char <= '힣':
            # 초,중,종성 분해
            cho, jung, jong = decompose_hangul(char)
            # 초성만 있는 경우
            if cho and not jung and not jong:
                pos = find_char_position_with_fallback(cho, "korean")
                row, col = pos
                adjacent_chars = get_adjacent_chars(row, col, korean_layout)
                new_cho = random.choice([c for c in adjacent_chars if c in CHOSEONG])
                noisy_text[idx] = compose_hangul(new_cho)
            # 초성과 중성만 있는 경우
            elif cho and jung and not jong:
                part_choice = random.choice(['cho', 'jung'])  # 초성과 중성 중 어디에 노이즈를 넣을지 선택
                if part_choice == 'cho':  # 초성 선택
                    pos = find_char_position_with_fallback(cho, "korean")
                    row, col = pos
                    adjacent_chars = get_adjacent_chars(row, col, korean_layout)
                    new_cho = random.choice([c for c in adjacent_chars if c in CHOSEONG])
                    noisy_text[idx] = compose_hangul(new_cho, jung)
                else:  # 중성 선택
                    pos = find_char_position_with_fallback(jung, "korean")
                    row, col = pos
                    adjacent_chars = get_adjacent_chars(row, col, korean_layout)
                    new_jung = random.choice([c for c in adjacent_chars if c in JUNGSEONG])
                    noisy_text[idx] = compose_hangul(cho, new_jung)
            # 초성, 중성, 종성이 모두 있는 경우
            else:                
                new_cho = None
                new_jung = None
                new_jong = None
                part_choice = random.choice(['cho', 'jung', 'jong'])
                if part_choice == 'cho':  # 초성 선택
                    pos = find_char_position_with_fallback(cho, "korean")
                    row, col = pos
                    adjacent_chars = get_adjacent_chars(row, col, korean_layout)                    
                    new_cho = random.choice([c for c in adjacent_chars if c in CHOSEONG])        
                    #print(new_cho, jung, jong)            
                    #print("compose_hangul(new_cho, jung, jong): ",compose_hangul(new_cho, jung, jong))
                    noisy_text[idx] = compose_hangul(new_cho, jung, jong)
                elif part_choice == 'jung':  # 중성 선택
                    pos = find_char_position_with_fallback(jung, "korean")
                    row, col = pos
                    adjacent_chars = get_adjacent_chars(row, col, korean_layout)
                    new_jung = random.choice([c for c in adjacent_chars if c in JUNGSEONG])
                    #print(cho, new_jung, jong)
                    #print("compose_hangul(cho, new_jung, jong): ",compose_hangul(cho, new_jung, jong))
                    noisy_text[idx] = compose_hangul(cho, new_jung, jong)
                else:  # 종성 선택
                    pos = find_char_position_with_fallback(jong, "korean")
                    row, col = pos
                    adjacent_chars = get_adjacent_chars(row, col, korean_layout)
                    new_jong = random.choice([c for c in adjacent_chars if c in JONGSEONG])
                    #print(cho, jung, new_jong)
                    #print("compose_hangul(cho, jung, new_jong) ",compose_hangul(cho, jung, new_jong))
                    noisy_text[idx] = compose_hangul(cho, jung, new_jong)
                #print("adjacent_chars: ",adjacent_chars)
                #print("cho, jung, jong: ",cho, jung, jong)
                #print("new_cho, new_jung, new_jong: ",new_cho, new_jung, new_jong)
    return ''.join(noisy_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='Input file path containing the corpus text')
    parser.add_argument('--output_file', type=str, required=True, help='Output file path to save the noisy corpus')
    parser.add_argument('--noise_percentage', type=float, default=0.2, help='Percentage of characters to add noise to (0-100)')
    args = parser.parse_args()

    # corpus.txt 파일을 열어서 모든 line에 add_noise_to_text 함수를 적용하고 적용된 텍스트를 저장하는 코드
    input_file_path = args.input_file
    output_file_path = args.output_file
    noise_percentage = args.noise_percentage  # 노이즈를 줄 비율 (0-1 사이)

    total_lines = sum(1 for line in open(input_file_path, 'r', encoding='utf-8'))
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in tqdm(infile, total=total_lines, desc="Processing lines"):
            noisy_line = add_noise_to_text(line.strip(), noise_percentage)
            outfile.write(noisy_line + '\n')