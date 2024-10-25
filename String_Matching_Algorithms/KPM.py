# Function to create the Longest Prefix Suffix (LPS) array
def computeLPSArray(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

# KMP string matching algorithm
def KMPSearch(pattern, text):
    lps = computeLPSArray(pattern)
    i = 0  # index for text
    j = 0  # index for pattern
    matches = []

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return matches

# Function to count JD keyword matches in a resume
def countJDMatches(jd_keywords, resume_text):
    match_count = 0
    for keyword in jd_keywords:
        match_positions = KMPSearch(keyword, resume_text)
        if match_positions:
            match_count += 1
    return match_count

# Function to rank resumes based on JD keyword matches
def rankResumes(jd_keywords, resumes):
    resume_ranking = []
    for i, resume in enumerate(resumes):
        match_count = countJDMatches(jd_keywords, resume)
        resume_ranking.append((f'Resume {i+1}', match_count))
    
    # Sort resumes by the number of matches (highest first)
    resume_ranking.sort(key=lambda x: x[1], reverse=True)
    
    return resume_ranking

# Example usage with three resumes
jd_keywords = ["Machine Learning", "Python", "Data Science", "Kubernetes", "Cloud"]
resumes = [
    "Experienced Data Scientist with expertise in Python, Machine Learning, and large-scale data processing.",
    "Proficient in Kubernetes, Cloud technologies, and Python for automating and deploying applications.",
    "Passionate about Machine Learning and Data Science, with projects focused on Python and data analysis."
]

# Rank the resumes
ranked_resumes = rankResumes(jd_keywords, resumes)

# Display the ranked resumes
for rank, (resume_name, match_count) in enumerate(ranked_resumes, start=1):
    print(f"Rank {rank}: {resume_name} with {match_count} matches")
