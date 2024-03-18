# -*- coding: utf-8 -*-
"""Wanda Armadianti_VIX_ID/X Partners.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iTPtxj4cmD65-vNi71jQM9357PXKnUxb

# Import Library
"""

import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import StratifiedShuffleSplit
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

"""# Load Data"""

! gdown --id 1lDDUxarU9krRMWCLyMdDueGe5h8WF-Q2

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv('/content/FP Rakamin.csv')
df.head(10)

"""# Eksploring Data

## Check Data Type
"""

df.info()

"""## Statistical Summary"""

# Melihat rangkuman statistik dari kolom numerik
df.describe()

"""## Value Count"""

# Mengecek jumlah masing-masing value pada kolom kategorikal
numeric_columns = df.select_dtypes(include='object').columns

for column in numeric_columns:
    print(f"Value counts for {column}:\n{df[column].value_counts()}\n")

"""# Defining Target Column

Kolom yang akan dijadikan target adalah 'loan_status' karena dapat menunjukkan performa kredit dari debitur, dengan kata lain dapat menunjukkan kualitas kredit, apakah bisa disebut baik atau buruk. Berikut adalah penjelasan value-value dari kolom 'loan_status':
1. Current:Peminjam saat ini masih membayar angsuran sesuai jadwal dan belum mengalami keterlambatan pembayaran
2. Fully Paid: Peminjam telah melunasi pinjaman sepenuhnya dengan pembayaran yang telah dijadwalkan.
3. Charged Off: Peminjam dianggap tidak mampu melunasi pinjaman, dan pinjaman dianggap sebagai kerugian oleh pemberi pinjaman.
4. Late (31-120 days): Peminjam memiliki keterlambatan pembayaran selama 31-120 hari. Ini menunjukkan bahwa pembayaran telah melewati batas jatuh tempo.
5. In Grace Period: Peminjam mungkin memiliki batas waktu tambahan untuk membayar (grace period), meskipun pembayaran telah lewat batas jatuh tempo.
6. Does not meet the credit policy. Status: Fully Paid: Meskipun peminjam tidak memenuhi kebijakan kredit tertentu, mereka telah melunasi pinjaman sepenuhnya.
7. Late (16-30 days): Peminjam memiliki keterlambatan pembayaran selama 16-30 hari.
8. Default: Default menunjukkan bahwa peminjam gagal memenuhi kewajiban pembayaran, dan pinjaman dianggap macet.
9. Does not meet the credit policy. Status: Charged Off: Meskipun peminjam tidak memenuhi kebijakan kredit tertentu, pinjaman dianggap sebagai kerugian oleh pemberi pinjaman.

Diasumsikan bahwa pinjaman yang baik adalah pinjaman yang telah atau sedang dibayar, sedangkan pinjaman yang buruk adalah pinjaman gagal bayar atau telat bayar. Oleh karena itu, value yang dilabeli "good" adalah sebagai berikut:
- Current
- Fully Paid
- In Grace Period
- Does not meet the credit policy. Status: Fully Paid

Sedangkan sisanya akan dilabeli "bad"
"""

good_loan = ['Current',
              'Fully Paid',
              'In Grace Period',
              'Does not meet the credit policy. Status:Fully Paid']
df['loan_status'] = np.where(df['loan_status'].isin(good_loan), 'good', 'bad')
df.head()

"""# Feature Selection

Feature Selection bertujuan untuk memilih kolom yang paling relevan atau signifikan untuk membangun model. Tujuan utama dari feature selection adalah meningkatkan kinerja model dengan mengurangi dimensi data, mengurangi kompleksitas model, meningkatkan interpretabilitas, dan mengurangi risiko overfitting. Beberapa cara yang dilakukan antara lain:
- Menghapus kolom yang terdiri dari banyak missing value
- Menghapus kolom yang terdiri dari banyak value unik
- Menghapus kolom yang tidak diperlukan

## Handle Missing Value
"""

# Mengecek jumlah missing value pada semua kolom
null_value = df.isnull().sum()
null_value

# Kolom dengan jumlah jumlah missing value <50% diatasi dengan cara mengisikan nilai modus masing-masing kolom pada value yang kosong
df['emp_title'] = df['emp_title'].fillna(df['emp_title'].mode().iloc[0])
df['emp_length'] = df['emp_length'].fillna(df['emp_length'].mode().iloc[0])
df['title'] = df['title'].fillna(df['title'].mode().iloc[0])
df['delinq_2yrs'] = df['delinq_2yrs'].fillna(df['delinq_2yrs'].mode().iloc[0])
df['earliest_cr_line'] = df['earliest_cr_line'].fillna(df['earliest_cr_line'].mode().iloc[0])
df['inq_last_6mths'] = df['inq_last_6mths'].fillna(df['inq_last_6mths'].mode().iloc[0])
df['open_acc'] = df['open_acc'].fillna(df['open_acc'].mode().iloc[0])
df['pub_rec'] = df['pub_rec'].fillna(df['pub_rec'].mode().iloc[0])
df['revol_util'] = df['revol_util'].fillna(df['revol_util'].mode().iloc[0])
df['total_acc'] = df['total_acc'].fillna(df['total_acc'].mode().iloc[0])
df['last_pymnt_d'] = df['last_pymnt_d'].fillna(df['last_pymnt_d'].mode().iloc[0])
df['last_credit_pull_d'] = df['last_credit_pull_d'].fillna(df['last_credit_pull_d'].mode().iloc[0])
df['collections_12_mths_ex_med'] = df['collections_12_mths_ex_med'].fillna(df['collections_12_mths_ex_med'].mode().iloc[0])
df['acc_now_delinq'] = df['acc_now_delinq'].fillna(df['acc_now_delinq'].mode().iloc[0])
df['tot_coll_amt'] = df['tot_coll_amt'].fillna(df['tot_coll_amt'].mode().iloc[0])
df['tot_cur_bal'] = df['tot_cur_bal'].fillna(df['tot_cur_bal'].mode().iloc[0])
df['total_rev_hi_lim'] = df['total_rev_hi_lim'].fillna(df['total_rev_hi_lim'].mode().iloc[0])

# Kolom dengan jumlah jumlah missing value >50% diatasi dengan cara menghapus kolom-kolom tersebut
df.drop(['desc',
         'mths_since_last_delinq',
         'mths_since_last_record',
         'next_pymnt_d',
         'mths_since_last_major_derog',
         'annual_inc_joint',
         'dti_joint',
         'verification_status_joint',
         'open_acc_6m',
         'open_il_6m',
         'open_il_12m',
         'open_il_24m',
         'mths_since_rcnt_il',
         'total_bal_il',
         'il_util',
         'open_rv_12m',
         'open_rv_24m',
         'max_bal_bc',
         'all_util',
         'inq_fi',
         'total_cu_tl',
         'inq_last_12m'], axis=1, inplace=True)

# Mengecek ulang jumlah missing value pada semua kolom
null_value = df.isnull().sum()
null_value

"""## Handle Unique Column"""

# Mengecek jumlah nilai unik pada semua kolom
unique_value = df.nunique()
unique_value

# Menghapus kolom yang jumlah nilai uniknya 1 atau terlalu banyak
df.drop(['Unnamed: 0',
         'id',
         'member_id',
         'funded_amnt',
         'funded_amnt_inv',
         'dti',
         'total_rec_late_fee',
         'tot_coll_amt',
         'installment',
         'url',
         'title',
         'revol_bal',
         'emp_title',
         'annual_inc',
         'out_prncp',
         'out_prncp_inv',
         'total_pymnt',
         'total_pymnt_inv',
         'total_rec_prncp',
         'total_rec_int',
         'recoveries',
         'collection_recovery_fee',
         'last_pymnt_amnt',
         'tot_cur_bal',
         'policy_code',
         'application_type',
         'total_rev_hi_lim'], axis=1, inplace=True)

# Mengecek ulang jumlah nilai unik pada semua kolom
unique_value = df.nunique()
unique_value

"""## Useless Column

Kolom yang tidak diperlukan untuk analisis lebih lanjut sebaiknya dihapus agar mendapat performa model yang baik.
"""

df.drop(['sub_grade',
         'zip_code',
         'earliest_cr_line'], axis=1, inplace=True)

"""# Change Data Type

Pada tahap ini, data diubah menjadi format yang lebih sesuai untuk analisis lebih lanjut.
- Tipe kolom 'term' dan 'emp_length' diubah menjadi numeric dengan penyesuaian format tertentu
- Tipe kolom 'issue_d', 'last_pymnt_d', dan 'last_credit_pull_d' diubah menjadi datetime

Kolom 'term'
"""

df['term_months'] = df['term'].str.replace(' months', '')
df['term_months'] = df['term_months'].astype(int)
df.drop('term', axis=1, inplace=True)

"""Kolom 'emp_length'"""

df['emp_length_years'] = df['emp_length'].str.replace('\+ years', '')
df['emp_length_years'] = df['emp_length_years'].str.replace('< 1 year', str(0))
df['emp_length_years'] = df['emp_length_years'].str.replace(' years', '')
df['emp_length_years'] = df['emp_length_years'].str.replace(' year', '')
df['emp_length_years'] = df['emp_length_years'].astype(int)
df.drop('emp_length', axis=1, inplace=True)

"""Kolom 'issue_d', 'earliest_cr_line', 'last_pymnt_d', dan 'last_credit_pull_d'"""

df['issue_d'] = pd.to_datetime(df['issue_d'], format='%b-%y')
df['last_pymnt_d'] = pd.to_datetime(df['last_pymnt_d'], format='%b-%y')
df['last_credit_pull_d'] = pd.to_datetime(df['last_credit_pull_d'], format='%b-%y')

df.head()

"""# Handle Duplicated Data"""

duplicated_data = df.duplicated().sum()
duplicated_data

"""Tidak ada data duplikat

# Handle Outliers
"""

# Menghapus outlier menggunakan Z-score dengan Threshold 3
def remove_outliers_zscore_loop(df, threshold=3):
    outliers = []
    for col in df.select_dtypes(include='number').columns:
        z_scores = np.abs((df[col] - df[col].mean()) /df[col].std())
        outliers.append(z_scores <= threshold)
    outliers = np.all(outliers, axis=0)
    no_outliers = df[outliers]
    return no_outliers

df = remove_outliers_zscore_loop(df)

"""# Univariate Analysis

## Categorical Columns
"""

for column in df.select_dtypes(include='object'):
    plt.figure(figsize=(18,8))
    ax = sns.countplot(x=df[column], edgecolor='k', color='#085A7D')
    plt.xlabel(column)
    plt.ylabel('Frequency')

    # Menambahkan label persentase di atas setiap bar
    total = len(df[column])
    for p in ax.patches:
        percentage = '{:.1f}%'.format(100 * p.get_height() / total)
        x = p.get_x() + p.get_width() / 2
        y = p.get_height() + 0.005 * total  # Sesuaikan dengan posisi label
        ax.annotate(percentage, (x, y), ha='center')

    plt.show()

"""## Numerical Columns"""

for column in df.select_dtypes(include=np.number):
    plt.figure(figsize=(14, 10))
    plt.hist(df[column], bins=20, edgecolor='k', color='#085A7D')
    plt.title(f'Histogram of {column}')
    plt.ylabel('Frequency')
    plt.xlabel(column)

    total = len(df[column])
    for rect in plt.gca().patches:
        height = rect.get_height()
        percentage = '{:.1f}%'.format(100 * height / total)
        plt.text(rect.get_x() + rect.get_width() / 2, height + 0.005*total, percentage, ha='center')
    plt.show()

"""## Date Columns"""

for column in df.select_dtypes(include='datetime'):
    plt.figure(figsize=(12, 6))
    grouped_data = df.groupby(df[column].dt.year).size().reset_index(name='count')
    line_plot = sns.lineplot(x=grouped_data[column], y=grouped_data['count'], marker='o')
    plt.title(f'Jumlah Data per Tahun Kolom "{column}"')
    plt.xlabel('Tahun')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

"""# Bivariate Analysis

## Correlation All Pair Independent Columns

Untuk melihat korelasi antar pasangan kolom independen, digunakan correlation plot dan heatmap matrix. Angka korelasi dapat dibagi menjadi 5 kategori berikut:
1. Strong Positive Correlation (0,5 hingga 1): Ketika angka korelasinya 1, itu menunjukkan hubungan linear positif sempurna antara dua variabel. Ini berarti ketika satu variabel naik, yang lain juga naik secara linier.
2. Weak Positive Correlation (0 hingga 0,5): Ketika angka korelasi berada di antara 0 dan 1 (tidak mencapai 1), itu menunjukkan hubungan positif antara dua variabel, tetapi tidak sempurna. Semakin mendekati 1, semakin kuat hubungannya.
3. No Correlation (0): Angka korelasi 0 menunjukkan bahwa tidak ada hubungan linier antara dua variabel. Ini berarti perubahan dalam satu variabel tidak memiliki pengaruh linier pada variabel lainnya.
4. Weak Negative Correlation (0 hingga -0,5): Ketika angka korelasi berada di antara 0 dan -1 (tidak mencapai -1), itu menunjukkan hubungan negatif antara dua variabel, tetapi tidak sempurna. Semakin mendekati -1, semakin kuat hubungannya.
5. Strong Negative Correlation(-0,5 hingga -1): Ketika angka korelasinya -1, itu menunjukkan hubungan linear negatif sempurna antara dua variabel. Ini berarti ketika satu variabel naik, yang lain turun secara linier.
"""

numeric_df = df.select_dtypes(include=[np.number])
cor_data = numeric_df.corr(method='pearson')
cor_data.round(2)

plt.figure(figsize=(40, 40))
sns.heatmap(cor_data, annot=True, cmap='Blues', vmin=-1, vmax=1)
plt.title('Heatmap')
plt.show()

"""Dari heatmap matrix di atas, dapat dilihat bahwa yang memiliki korelasi tinggi adalah kolom total_acc dan open_acc dengan nilai korelasi 0,66.

## Correlation Columns w/Target Column
"""

excluded_columns = ['loan_amnt', 'int_rate', 'issue_d', 'revol_util', 'last_pymnt_d', 'last_credit_pull_d']

for column in df.columns:
    if column != 'loan_status' and column not in excluded_columns:
        plt.figure(figsize=(10, 6))
        subset_df = df[[column, 'loan_status']]
        subset_df = subset_df[subset_df[column].isin(subset_df[column].value_counts().index)]
        subset_df = pd.crosstab(subset_df[column], subset_df['loan_status'])
        colors = ['#00A8B6', '#085A7D']
        subset_df.plot(kind='bar', stacked=True, figsize=(10, 6), color=colors)
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.title(f'Stacked Bar Chart for {column}')
        plt.legend(title='loan_status', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()

"""# Labeling

Mengubah kolom 'mths_since_issue', 'mths_since_last_pymnt', dan 'mths_since_last_credit_pull' dari format date menjadi format numeric agar dapat dilakukan label encoding dengan baik. Caranya adalah dengan menghitung jumlah bulan tertera hingga waktu saat ini.
"""

df['mths_since_issue'] = round(pd.to_numeric((pd.to_datetime('2024-01-01') - df['issue_d']) / np.timedelta64(1, 'M')))
df['mths_since_last_pymnt'] = round(pd.to_numeric((pd.to_datetime('2024-01-01') - df['last_pymnt_d']) / np.timedelta64(1, 'M')))
df['mths_since_last_credit_pull'] = round(pd.to_numeric((pd.to_datetime('2024-01-01') - df['last_credit_pull_d']) / np.timedelta64(1, 'M')))
df.drop(['issue_d'], axis=1, inplace=True)
df.drop(['last_pymnt_d'], axis=1, inplace=True)
df.drop(['last_credit_pull_d'], axis=1, inplace=True)
df.head()

df_encoded = df.copy()
label_encoder = LabelEncoder()
for column in df_encoded.select_dtypes(include='object').columns:
    df_encoded[column] = label_encoder.fit_transform(df_encoded[column])
df_encoded.head()

# Mengecek tipe data setelah encoding
df_encoded.info()

"""# Data Balancing

Sebelum data dipisahkan menjadi train set dan test set hingga digunakan ke dalam model machine learning, data harus diseimbangkan. Data harus diseimbangkan berdasarkan jumlah dari kolom dependen yang menjadi tujuan, yaitu kolom ‘loan_status’. Penyeimbangan dilakukan dengan menggunakan instance dari RandomOverSampler() milik library imblearn, dengan memasukkan dataframe feature dan label sebagai input untuk dilakukan penyeimbangan.
"""

df_encoded['loan_status'].value_counts()

"""Ketika jumlah value dicek, didapatkan fakta bahwa value '1' yang merepresentasikan ‘good’ memiliki jumlah 383259 yang mana jauh lebih banyak daripada value '0' yang merepresentasikan nilai ‘bad’. Oleh karena itu, value harus diseimbangkan sehingga jumlahnya sama menjadi 383259

"""

X = df_encoded.drop('loan_status', axis=1)
y = df_encoded['loan_status']

balanced = RandomOverSampler(random_state=42)
X_balanced, y_balanced = balanced.fit_resample(X, y)
y_balanced.value_counts()

"""Hasilnya, didapatkan data feature dan label yang telah diseimbangkan, sehingga sekarang value ‘bad’ (0) dan ‘good’ (1) telah seimbang menjadi 383259 baris data.

# Data Splitting

Sebelum dimasukkan ke dalam model klasifikasi, data harus dipisahkan/dipotong menjadi train set dan test set. Ada 4 dataset yang akan dihasilkan, yaitu X_train dan y_train, serta X_test dan y_test. Pemisahan dilakukan dengan menggunakan test_size = 30%, yaitu 30% dari data akan dialokasikan ke dataset uji (X_test dan y_test), sedangkan 70% sisanya akan digunakan sebagai dataset pelatihan (X_train dan y_train). Data pelatihan (X_train dan y_train) akan digunakan untuk melatih model, dan data uji (X_test dan y_test) akan digunakan untuk menguji kinerja model tersebut.
"""

X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.3, random_state=42, stratify=y_balanced)

"""# Feature Scalling

Feature scaling digunakan untuk menyamakan skala pada data numerik di dataset agar nilainya tidak terlalu jauh dibandingkan data lainnya. Kolom apa saja yang perlu dilakukan feature scaling dapat dievaluasi dari nilai persebaran nilainya.
"""

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

X_train

X_test

"""# Classification Model

## Logistic Regression
"""

logreg = LogisticRegression()
logreg.fit(X_train, y_train)
y_pred_logreg = logreg.predict(X_test)
print('Classification report:\n', metrics.classification_report(y_test, y_pred_logreg))

fpr, tpr, thresholds = roc_curve(y_test, y_pred_logreg)
roc_auc = roc_auc_score(y_test, y_pred_logreg)

plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

"""## Neural Network"""

nn =  MLPClassifier(alpha=1, max_iter=1000)
nn.fit(X_train, y_train)
y_pred_nn = nn.predict(X_test)
print('Classification report:\n', metrics.classification_report(y_test, y_pred_nn))

fpr, tpr, thresholds = roc_curve(y_test, y_pred_nn)
roc_auc = roc_auc_score(y_test, y_pred_nn)

plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

"""## Decision Tree"""

dtree = DecisionTreeClassifier()
dtree.fit(X_train, y_train)
y_pred_dtree = dtree.predict(X_test)
print('Classification report:\n', metrics.classification_report(y_test, y_pred_dtree))

fpr, tpr, thresholds = roc_curve(y_test, y_pred_dtree)
roc_auc = roc_auc_score(y_test, y_pred_dtree)

plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

"""## Random Forest"""

rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print('Classification report:\n', metrics.classification_report(y_test, y_pred_rf))

fpr, tpr, thresholds = roc_curve(y_test, y_pred_rf)
roc_auc = roc_auc_score(y_test, y_pred_rf)

plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

"""## K-Nearest Neighbors"""

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)
print('Classification report:\n', metrics.classification_report(y_test, y_pred_knn))

fpr, tpr, thresholds = roc_curve(y_test, y_pred_knn)
roc_auc = roc_auc_score(y_test, y_pred_knn)

plt.figure(figsize=(8, 8))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = {:.2f})'.format(roc_auc))
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()

"""## Conclusion

Dari 5 model klasifikasi di atas, model dengan performa terbaik untuk melakukan prediksi terhadap credit risk adalah Random Forest dengan f1-score=0,97 dan score ROC-AUC=0,97
"""