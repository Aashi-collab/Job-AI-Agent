def analyze_weakness(scores):

    try:
        if not scores:
            return "No data available"

        avg = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)

        # -----------------------------
        # 📊 PERFORMANCE ANALYSIS
        # -----------------------------
        if avg >= 8:
            message = "Excellent performance. You have strong understanding of concepts."
        elif avg >= 5:
            message = "Good performance, but there is room for improvement."
        else:
            message = "Performance is below expectations. Focus on fundamentals."

        # -----------------------------
        # 📉 CONSISTENCY ANALYSIS
        # -----------------------------
        if max_score - min_score > 4:
            consistency = "Your performance is inconsistent. Try to maintain stability."
        else:
            consistency = "Your performance is consistent."

        # -----------------------------
        # 📌 FINAL MESSAGE
        # -----------------------------
        return f"""
{message}

📊 Average Score: {avg:.2f}/10
📉 Lowest Score: {min_score}/10
📈 Highest Score: {max_score}/10

💡 Insight:
{consistency}
"""

    except Exception as e:
        return f"Error analyzing performance: {str(e)}"