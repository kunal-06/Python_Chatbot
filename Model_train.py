# %%
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np 



# %%
df1 = pd.read_csv("processed_data_part1.csv")
df2 = pd.read_csv("processed_data_part2.csv")
df3 = pd.read_csv("processed_data_part3.csv")



df = pd.concat([df1,df2,df3],ignore_index=True)

dialog  = pd.read_csv("Quick_Dialog.csv")
dialog_pr = dialog.drop(dialog.columns[[0]], axis=1)
dialog_pr.columns = ['processed_question','answer']



combined_df = pd.concat([df, dialog_pr],ignore_index=True)
combined_df.head(10)

# %%
vectorizer = TfidfVectorizer(max_features=5000,ngram_range=(1,2),dtype=np.float32)
X_matrix = vectorizer.fit_transform(combined_df.processed_question.values)
X_matrix.shape


# %%

def find_best_answer(user_query):
    query_vector = vectorizer.transform([user_query])
    
    similarities = cosine_similarity(query_vector, X_matrix)
    
    best_match_index = similarities.argmax()
    best_match_score = similarities[0, best_match_index]
    
    if best_match_score > 0.5: 
        return combined_df["answer"].iloc[best_match_index]
    else:
        return "I'm sorry, I couldn't find a matching answer."




# %%
