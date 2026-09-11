from flask import Flask, render_template, request, jsonify
from collections import Counter

app = Flask(__name__)

# حروف صدادار
PERSIAN_VOWELS = set("اآایوئ")
ENGLISH_VOWELS = set("aeiou")


def analyze_name(name):
    name = name.strip()

    # فقط حروف را نگه می‌داریم
    letters = [char for char in name if char.isalpha()]

    # برای تحلیل، حروف انگلیسی را کوچک می‌کنیم
    normalized = [char.lower() for char in letters]

    # تعداد تکرار هر حرف
    letter_counts = Counter(normalized)

    # تعداد کل حروف
    total_letters = len(normalized)

    # تعداد حروف منحصربه‌فرد
    unique_letters = len(set(normalized))

    # شمارش صدادار و بی‌صدا
    vowels = 0
    consonants = 0

    for char in normalized:
        if char in PERSIAN_VOWELS or char in ENGLISH_VOWELS:
            vowels += 1
        else:
            consonants += 1

    # پرتکرارترین حرف
    if letter_counts:
        max_count = max(letter_counts.values())

        most_common = [
            char
            for char, count in letter_counts.items()
            if count == max_count
        ]
    else:
        max_count = 0
        most_common = []

    # بررسی پالیندروم
    palindrome_text = "".join(normalized)

    is_palindrome = (
        len(palindrome_text) > 0
        and palindrome_text == palindrome_text[::-1]
    )

    # نام برعکس
    reversed_name = name[::-1]

    return {
        "name": name,
        "letter_counts": dict(letter_counts),
        "total_letters": total_letters,
        "unique_letters": unique_letters,
        "vowels": vowels,
        "consonants": consonants,
        "most_common_letters": most_common,
        "most_common_count": max_count,
        "is_palindrome": is_palindrome,
        "reversed_name": reversed_name
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "error": "نام ارسال نشده است."
        }), 400

    name = data["name"]

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "لطفاً یک نام معتبر وارد کنید."
        }), 400

    result = analyze_name(name)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)