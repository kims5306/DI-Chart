import base64

# CI.png 파일을 base64로 변환
with open('CI.png', 'rb') as f:
    base64_string = base64.b64encode(f.read()).decode()

# base64 문자열을 파일에 저장
with open('ci_base64.txt', 'w') as f:
    f.write(base64_string)

print("CI.png가 base64로 변환되어 ci_base64.txt에 저장되었습니다.")
print(f"Base64 길이: {len(base64_string)} 문자")
print("첫 100문자:", base64_string[:100])
