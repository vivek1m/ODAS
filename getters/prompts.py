from groq import Groq


prompt = """
Provide a paragraph answer for {} in {} words for the
identified cancer type."""

qna = """
<context>
{}
</context>
Question: {}
"""
model_name = ""


def get_drug(context,cancer):
    drug = llm.chat.completions.create(
        
        messages=[            
            {
                'role':'system',
                'content': prompt.format("Drug Use Advisory", "50")
            }
        ],
        model=model_name,
    )
    return drug

def get_diagnosis(context,cancer):
    diagnosis = llm.chat.completions.create(
        messages=[
            {
                'role':'system',
                'content': prompt.format("Diagnosis" , "100")
            }
        ],
        model=model_name,
    )
    return diagnosis

def q_n_a(context,query):
    answer = llm.chat.completions.create(
        messages=[
            {
                'role':'system',
                'content': qna.format(context , query)
            }
        ],
        model=model_name,
    )
    return answer
