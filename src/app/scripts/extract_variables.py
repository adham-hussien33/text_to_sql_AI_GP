import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")


patterns = {
    "email": [{"TEXT": {"REGEX": r"[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+"}}],
    "departmentId": [{"IS_DIGIT": True}],
    "employeeId": [{"IS_DIGIT": True}],
    "managerId": [{"IS_DIGIT": True}],
    "jobId": [{"IS_DIGIT": True}],
    "applicantId": [{"IS_DIGIT": True}],
    "limit": [{"IS_DIGIT": True}],
    "status": [{"LOWER": {"IN": ["pending", "completed", "open", "closed", "active"]}}],
    "gender": [{"LOWER": {"IN": ["male", "female", "other"]}}],
    "domain": [{"TEXT": {"REGEX": r"@[a-zA-Z0-9-.]+"}}]
}

def extract_variables(text, required_fields):
    doc = nlp(text)
    extracted = {}
    
    for field in required_fields:
        # Check if we have a pattern for this field
        if field in patterns:
            matcher = Matcher(nlp.vocab)
            matcher.add(field, [patterns[field]])
            matches = matcher(doc)
            if matches:
                # Get the first match found
                span = doc[matches[0][1]:matches[0][2]]
                extracted[field] = span.text
    return extracted