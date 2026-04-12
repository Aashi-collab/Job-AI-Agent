def resume_agent(job, user_profile):

    skills = user_profile.get("skills", [])
    resume = user_profile.get("resume", "")

    return f"""
Resume Tailored for {job['title']} at {job['company']}

Skills:
{", ".join(skills)}

Summary:
A motivated candidate with strong foundation in {", ".join(skills)}.

Experience:
{resume[:300] if resume else "Fresher with project experience"}

Objective:
Seeking a role as {job['title']} to apply skills and grow professionally.
"""