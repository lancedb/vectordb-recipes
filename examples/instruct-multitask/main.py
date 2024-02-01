""" Install lancedb with instructor embedding support 
    copy this and paste it in the terminal, and install additional dependencies via requirements.txt file
     
       pip install git+https://github.com/lancedb/lancedb.git@main#subdirectory=python
"""

import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from lancedb.embeddings import InstructorEmbeddingFunction

instructor = (
    get_registry()
    .get("instructor")
    .create(
        source_instruction="represent the document for retreival",
        query_instruction="represent the document for most similar definition",
    )
)


class Schema(LanceModel):
    vector: Vector(instructor.ndims()) = instructor.VectorField()
    text: str = instructor.SourceField()


# Creating LanceDB table
db = lancedb.connect("~/.lancedb")
tbl = db.create_table("intruct-multitask", schema=Schema, mode="overwrite")

data_f1 = [
    {
        "text": "Aspirin is a widely-used over-the-counter medication known for its anti-inflammatory and analgesic properties. It is commonly used to relieve pain, reduce fever, and alleviate minor aches and pains."
    },
    {
        "text": "Amoxicillin is an antibiotic medication commonly prescribed to treat various bacterial infections, such as respiratory, ear, throat, and urinary tract infections. It belongs to the penicillin class of antibiotics and works by inhibiting bacterial cell wall synthesis."
    },
    {
        "text": "Atorvastatin is a lipid-lowering medication used to manage high cholesterol levels and reduce the risk of cardiovascular events. It belongs to the statin class of drugs and works by inhibiting an enzyme involved in cholesterol production in the liver."
    },
    {
        "text": "The Theory of Relativity is a fundamental physics theory developed by Albert Einstein, consisting of the special theory of relativity and the general theory of relativity. It revolutionized our understanding of space, time, and gravity."
    },
    {
        "text": "Photosynthesis is a vital biological process by which green plants, algae, and some bacteria convert light energy into chemical energy in the form of glucose, using carbon dioxide and water."
    },
    {
        "text": "The Big Bang Theory is the prevailing cosmological model that describes the origin of the universe. It suggests that the universe began as a singularity and has been expanding for billions of years."
    },
    {
        "text": "Compound Interest is the addition of interest to the principal sum of a loan or investment, resulting in the interest on interest effect over time."
    },
    {
        "text": "Stock Market is a financial marketplace where buyers and sellers trade ownership in companies, typically in the form of stocks or shares."
    },
    {
        "text": "Inflation is the rate at which the general level of prices for goods and services is rising and subsequently purchasing power is falling."
    },
    {
        "text": "Diversification is an investment strategy that involves spreading your investments across different asset classes to reduce risk."
    },
    {
        "text": "Liquidity refers to how easily an asset can be converted into cash without a significant loss of value. It's a key consideration in financial management."
    },
    {
        "text": "401(k) is a retirement savings plan offered by employers, allowing employees to save and invest a portion of their paycheck before taxes."
    },
    {
        "text": "Ballet is a classical dance form that originated in the Italian Renaissance courts of the 15th century and later developed into a highly technical art."
    },
    {
        "text": "Rock and Roll is a genre of popular music that originated and evolved in the United States during the late 1940s and early 1950s, characterized by a strong rhythm and amplified instruments."
    },
    {
        "text": "Cuisine is a style or method of cooking, especially as characteristic of a particular country, region, or establishment."
    },
    {"text": "Renaissance was a cultural, artistic, and intellectual movement that"},
    {
        "text": "Neutrino is subatomic particles with very little mass and no electric charge. They are produced in various nuclear reactions, including those in the Sun, and play a significant role in astrophysics and particle physics."
    },
    {
        "text": "Higgs Boson is a subatomic particle that gives mass to other elementary particles. Its discovery was a significant achievement in particle physics."
    },
    {
        "text": "Quantum Entanglement is a quantum physics phenomenon where two or more particles become connected in such a way that the state of one particle is dependent on the state of the other(s), even when they are separated by large distances."
    },
    {
        "text": "Genome Sequencing is the process of determining the complete DNA sequence of an organism's genome. It has numerous applications in genetics, biology, and medicine."
    },
]

tbl.add(data_f1)

# LanceDB supports full text search, so there is no need of embedding the Query manually
query = "amoxicillin"
result = tbl.search(query).limit(1).to_pandas()

# printing the output
print(result)


#########################################################################################################################
################# SAME INPUT DATA WITH DIFFERENT INSTRUCTION PAIR #######################################################
#########################################################################################################################

# uncomment the below code to check for different instruction pair on the same data

"""instructor = get_registry().get("instructor").create(
                            source_instruction="represent the captions",
                            query_instruction="represent the captions for retrieving duplicate captions"
                            )

class Schema(LanceModel):
    vector: Vector(instructor.ndims()) = instructor.VectorField()
    text: str = instructor.SourceField()

db = lancedb.connect("~/.lancedb")
tbl = db.create_table("intruct-multitask", schema=Schema, mode="overwrite")

data_f2 = [
    {"text": "Aspirin is a widely-used over-the-counter medication known for its anti-inflammatory and analgesic properties. It is commonly used to relieve pain, reduce fever, and alleviate minor aches and pains."},
    {"text": "Amoxicillin is an antibiotic medication commonly prescribed to treat various bacterial infections, such as respiratory, ear, throat, and urinary tract infections. It belongs to the penicillin class of antibiotics and works by inhibiting bacterial cell wall synthesis."},
    {"text": "Atorvastatin is a lipid-lowering medication used to manage high cholesterol levels and reduce the risk of cardiovascular events. It belongs to the statin class of drugs and works by inhibiting an enzyme involved in cholesterol production in the liver."},
    {"text": "The Theory of Relativity is a fundamental physics theory developed by Albert Einstein, consisting of the special theory of relativity and the general theory of relativity. It revolutionized our understanding of space, time, and gravity."},
    {"text": "Photosynthesis is a vital biological process by which green plants, algae, and some bacteria convert light energy into chemical energy in the form of glucose, using carbon dioxide and water."},
    {"text": "The Big Bang Theory is the prevailing cosmological model that describes the origin of the universe. It suggests that the universe began as a singularity and has been expanding for billions of years."},
    {"text": "Compound Interest is the addition of interest to the principal sum of a loan or investment, resulting in the interest on interest effect over time."},
    {"text": "Stock Market is a financial marketplace where buyers and sellers trade ownership in companies, typically in the form of stocks or shares."},
    {"text": "Inflation is the rate at which the general level of prices for goods and services is rising and subsequently purchasing power is falling."},
    {"text": "Diversification is an investment strategy that involves spreading your investments across different asset classes to reduce risk."},
    {"text": "Liquidity refers to how easily an asset can be converted into cash without a significant loss of value. It's a key consideration in financial management."},
    {"text": "401(k) is a retirement savings plan offered by employers, allowing employees to save and invest a portion of their paycheck before taxes."},
    {"text": "Ballet is a classical dance form that originated in the Italian Renaissance courts of the 15th century and later developed into a highly technical art."},
    {"text": "Rock and Roll is a genre of popular music that originated and evolved in the United States during the late 1940s and early 1950s, characterized by a strong rhythm and amplified instruments."},
    {"text": "Cuisine is a style or method of cooking, especially as characteristic of a particular country, region, or establishment."},
    {"text": "Renaissance was a cultural, artistic, and intellectual movement that"},
    {"text": "Neutrino is subatomic particles with very little mass and no electric charge. They are produced in various nuclear reactions, including those in the Sun, and play a significant role in astrophysics and particle physics."},
    {"text": "Higgs Boson is a subatomic particle that gives mass to other elementary particles. Its discovery was a significant achievement in particle physics."},
    {"text": "Quantum Entanglement is a quantum physics phenomenon where two or more particles become connected in such a way that the state of one particle is dependent on the state of the other(s), even when they are separated by large distances."},
    {"text": "Genome Sequencing is the process of determining the complete DNA sequence of an organism's genome. It has numerous applications in genetics, biology, and medicine."},
]

tbl.add(data_f2)

#same query, but for the differently embed data
query = "amoxicillin"
result = tbl.search(query).limit(1).to_pandas()

#showing the result
print(result)

"""
