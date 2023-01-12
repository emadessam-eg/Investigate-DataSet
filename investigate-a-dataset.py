#!/usr/bin/env python
# coding: utf-8

# # Project: The Movie Data Analysis (TMDb)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# <li><a href="#limitations">Limitations</a></li> 
# </ul>

# <a id='intro'></a>
# # Introduction
# In this project, we are going to analyze data about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue we will be interested in finding answers to the following questions:
# 1. Who are the directors who most direct films?
# 2. Who are the most actors who have played a starring roles in movies?
# 3. How is the revenue associated to the average voting score?
# 4. How is the revenue associated to the different genres ?
# 5. How is the genres associated to the average voting score? and does this associacion reflect on the revenue?
# 6. Does the budget increase has an effect on revenue?
# 
# 
# ### Note:
# 1. The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.
# 
# 2. Certain columns, like ‘cast’ and ‘genres’, contain multiple values separated by pipe (|) characters.
# 
# 3. There are some odd characters in the ‘cast’ column. Don’t worry about cleaning them. You can leave them as is.

# # Start here

# In[1]:


# This cell to set up import statements for all of the packages that I plan to use.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# ### General Properties

# In[2]:


# LoadING data from tmbd-movies.csv file.
movie = pd.read_csv('tmdb-movies.csv')


# In[3]:


# Get information about the columns indcies , Data frame shape, the type of the values in each column and the number of each
# non-null values in each column
movie.info()


# In[4]:


# Check rondom sample of the newly created movie data frame checking the formating and other issues if exist
movie.sample(10)


# ## Data Cleaning :
# ### Note: 
# The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.
# 
# 1. Removal of unrequired columns including budget and revenue as they are modified to take inflation into account in budget_adj and revenue_adg. 
# 2. Deleting duplication, null, and zero values.
# 3. Rename the columns of budget_adj and revenue_adj (those columns consider the inflation for revenue and budget).
# 4. modify columns of cast and genre to split by "/" and take the first string after the split as it represents the prime cast and genre 

# In[5]:


# 1- Remove OF unrequired columns including budget and revenue as they are modified to take infilation into account
# in budget_adj and revenue_adg 
# Drop columns based on column index.
movie.drop(movie.columns[[0,1, 3,4,7,9,10,11,14,15]],axis = 1,inplace=True)
# Chech a 10 random rows as a sample for the whole data frame after the columns removal
movie.sample(10)  


# In[6]:


# Investigate duplications 
movie.duplicated().sum()


# In[7]:


# Investigate of null values in each columns after removing the unrequired columns
movie.isnull().sum()


# In[8]:


# Investigate the values that equal to zero in each column
(movie == 0).sum()


# In[9]:


# 2- Deleting duplicationed, null and zero values 
for x in movie.columns:
    movie = movie.drop_duplicates()
    movie = movie.loc[movie[x] != 0]
    movie = movie.dropna()
   


  


# In[10]:


# Check for the null values after the removal
movie.isnull().sum()


# In[11]:


# Check for the shape, the type of the values in each column and the number of each
# non-null values in each column in movie data frame after the removal step 
movie.info()


# In[12]:


# Check 10 rows rondom sample of movie data frame after deleting duplicationed, null and zero values
movie.sample(10)


# In[13]:


# Check all zero values are removed
(movie.runtime ==0 ).value_counts()


# In[14]:


## Check all zero values are removed (other way) 
(movie.runtime == 0 ).sum()


# In[15]:


# 3- Rename the columns of budget_adj and revenue_adj (thos columns take the infilation into cosidweration for revenue and budget)
movie.rename(columns = {'budget_adj':'budget', 'revenue_adj':'revenue'}, inplace = True)


# In[16]:


# Check the renamed columns 
movie.info()


# In[17]:


# 4. modify columns of cast and genre to split by "/" and take the first string after the split as it represents the prime cast and genre 
split_columns = ['cast', 'genres']

# apply split function to each column of each dataframe copy and using lambada as function
for c in split_columns:
    movie[c] = movie[c].apply(lambda x: x.split("|")[0])
      
    
    
   


# In[18]:


# Check the formating change after the value modification performed by taking 10 rondom rows as a sample
movie.sample(10)


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# ### Research Question 1:Who are the directors who most direct films?

# In[19]:


# Extract the list of directors with thier count values (here count value is the number of the times the director directs a movie)
directors = movie['director'].value_counts(dropna=True, sort=True)


# In[20]:


#Check the director list created 
directors.info()


# In[21]:


# Build a data frame from the created list and rename its columns
directors = directors.rename_axis('director').reset_index(name='counts')


# In[22]:


# Check 10 rows as a rondom sample for the created data frame 
directors.sample(10)


# In[23]:


# Extract onyly a DF with the directors contributs in produs=cing films more than 15 times
directors_top = directors.where(directors['counts'] >15)


# In[24]:


# Check the created data frame as a whole
directors_top.info()


# In[25]:


# Check to quickly observe the NaN values
directors_top


# In[26]:


# Drop the NAN values from the top list of directors 
directors_top.dropna(inplace = True)


# In[27]:


# Check the created data frame according to the removal criteria performed 
directors_top


# ##### The table above shows the top-ranked directors who direct higher numbers of movies. It can be easily noticed that Steven Spielberg is at the top of the list..

# In[28]:


# Plot scatter diagram showing the directors ranking order
directors_top.plot(x="director", y="counts", kind="bar");
plt.legend()
plt.ylabel('The number of the directed movies')
plt.title('The top list of directors who direct movies')
plt.grid(True)


# #### A bar chart visually illustrates the result obtained from the above table. Steven Spielberg has the highest bar.

# ### Research Question 2:Who are the most actors who have played a starring roles in movies?

# In[29]:


# Extract actors list from movie data frame with their value counts (The number of times the actor starring a movie )
actors = movie['cast'].value_counts(dropna=True, sort=True)


# In[30]:


#Check the created list
actors.info()


# In[31]:


# Extract a data from actors list and rename columns
actors = actors.rename_axis('actor').reset_index(name='counts')


# In[32]:


# Check the created data frame
actors


# In[33]:


# Extract onyly a data frame with the actors contribut in starring films more than 26 times
actors_top = actors.where(actors['counts'] >26)


# In[34]:


# Check the created data frame 
actors_top


# In[35]:


# Delete the rows with NaN values 
actors_top.dropna(inplace=True)


# In[36]:


# Check the created list after removal of NaN values
actors_top


# #### A table shows the top-ranked stars who act in a large number of movies. It can be noticed that Nicolas Cage is at the top of the list.

# In[37]:


# Make the actor column as a row index to prepare for the pie chart
actors_top = actors_top.set_index('actor')


# In[38]:


# Check the data frame after the modification performed on 
actors_top


# In[39]:


# Creae a pie plot with actors list that starring more than 26 movies
plot =actors_top.plot.pie(y='counts', figsize=(10, 10))
plt.title('The actors who starring more than 26 movies')


# #### A pie chart illustrates visually the percentage of each star who acts in a larger number of movies. It can be noticed the percentages are close and Nicolas Cage has the higher portion of the pie (more contributions to the movies have been produced).

# In[77]:


# Create a horizontal bar plot with actors list that starring more than 26 movies
ax = actors_top.plot.barh(color = 'orange', )
plt.legend()
plt.xlabel('The number of the times the actor starring a movie')
plt.title('The top list of directors who direct movies')
plt.grid(True)


# #### A horizontal bar chart more illustrates visually the result highlited by the above table and pie chart.

# ### Research Question 3:How is the revenue associated to the average voting score?

# In[41]:


# Chek for the name of the columns in the original data frame movie
movie.head(0)


# In[42]:


# Extract a sub data frame from movie data frame containing revenue, vote_average and vote_counts
rev_vote = movie[["revenue", "vote_count",'vote_average']]


# In[43]:


# Set a criteria to not count rows with vote counts less than or equal 100
rev_vote = rev_vote[rev_vote["vote_count"] >100 ]


# In[44]:


# Check the created data frame
rev_vote.info()


# In[45]:


# Check the mean value of each column and have some statistical indication about the created data frame
rev_vote.describe()


# In[46]:


# Take a sub data for the movies with revenues less than the revenue mean 
# Then observe how the avg vote affected
rev_low = rev_vote[rev_vote["revenue"] <= 1.867443e+08 ]


# In[47]:


# Observe the mean values for the created data frame
rev_low.describe()


# #### A table shows a statistical characteristics of each column in rev_low data fram. The study focus on the association between the revenue and the average voting score and who voting score varies in the low and high revenue portions. The study for these variations taking the range of revenues under and above its mean in the vote_rev data frame as interperated below.

# In[62]:


# Define a function to plot a scatter diagram illustrates the correlation between the revenue and the average voting score      
def scatter_plot(df,i,j,k,l,m,z):
    ax = df.plot.scatter(x= i, y= j , color = k)
    ax.legend([i, j])
    ax.legend([i, j])
    plt.xlabel(l)
    plt.ylabel(m)
    plt.title(z)
    plt.grid(True)


# In[63]:


# Define a function to plot the density distribution for the average voting score for the created data frame rev_low
def kde_plot(df,i,j,l,m,n):
    df.plot(x=i, y=j, kind='kde');
    plt.legend()
    plt.xlabel(l)
    plt.ylabel(m)
    plt.title(n)
    plt.grid(True)


# In[69]:


# Plot a scatter diagram illustrates the correlation between the revenue and the average voting score 
scatter_plot(rev_low,'vote_average','revenue', 'plum','The average voting score', 'The revenue','The low revenues vs the average voting score' )


# #### A scatter diagram showing the correlation between the low revenues (the portion of revenues under the mean value of revenue in rev_vote data frame) and the corresponding average voting score.

# In[ ]:





# In[74]:


# Plot the density distribution for the average voting score for the created data frame rev_low
kde_plot(rev_vote,"revenue","vote_average",'The average voting score','The density counts for the average voting score','Figure shows the desity distribution for the average voting score for all revenues')
kde_plot(rev_low,"revenue","vote_average",'The average voting score','The density counts for the average voting score','Figure shows the desity distribution for the average voting score for low revenues')


# #### Density distribution curves for the voting score corresponding to the mean of the revenue in the rev_vote and rev_low data frames show that the mean of the voting score shifted left (becomes less in value from 6.32 to 6.24). Both curves show almost ideal normal distribution bell shapes.   

# In[51]:


# Take a sub data frame for the movies with revenues more than the revenue mean showed above for rev_vote
# Then observe how the avg vote affected
rev_high = rev_vote[rev_vote['revenue'] > 1.867443e+08]


# In[52]:


rev_high.describe()


#  ###### We can observe that the average voting score mean is increased  

# In[75]:


# Plot a scattter diagram showing the correlation between the revenue and the average voting score  
scatter_plot(rev_high,'vote_average','revenue', 'lime','The average voting score', 'The revenue','The high revenues vs the average voting score' )


# #### A scatter diagram showing the correlation between the high revenues (the portion of revenues under the mean value of revenue in the rev_vote data frame) and the corresponding average voting score.

# In[73]:


# Plot the density distribution for the average voting score for the created data frame rev_high
kde_plot(rev_vote,"revenue","vote_average",'The average voting score','The density counts for the average voting score','Figure shows the desity distribution for the average voting score for all revenues')
kde_plot(rev_high,"revenue","vote_average",'The average voting score','The density counts for the average voting score','Figure shows the desity distribution for the average voting score for high revenues')


# #### Density distribution curves for the voting score corresponding to the mean of the revenue in the rev_vote and rev_high data frames show that the mean of the voting score shifted right (becomes higher in value from 6.32 to 6.49). Both curves show almost ideal normal distribution bell shapes.

# In[68]:


# Comparing the mean of avg voting score for the ranges of high and low revenues
locations = [1, 2]
heights = [rev_low['vote_average'].mean(),rev_high['vote_average'].mean()]
labels = ['vote_avg_Low_rev', 'vote_avg_high_rev']
plt.bar(locations, heights, tick_label=labels, color = 'tan', width = 0.7)
plt.legend(['VoteAvgScore'])
plt.title('vote average score for high and low revenue')
plt.xlabel('averge vote')
plt.ylabel('vote average score');


# #### A simple bar chart illustrates and summarizes what has been mentioned above the mean voting score increased from the lower portion of the revenue to the higher one (from 6.24 to 6.49). Taking into consideration its value is 6.32 for the whole distribution of the revenue.

# ### Research Question 4:How is the revenue associated to the different genres ?

# In[59]:


# Refer to the original data frame movie to remember columns names
movie.head(0)


# In[60]:


# Extract a sub date fram from the movie data frame
rev_gen = movie[["revenue", "genres",'vote_count']]


# In[61]:


# Set criteria taking only the rows for vote count more than 100
rev_gen = rev_gen[rev_gen['vote_count'] > 100]


# In[62]:


# Check the chracteristices for the newly created through displaying 5 header lines
rev_gen.head(5)


# In[63]:


# Check the chracteristices for the newly created data frame
rev_gen.info()


# In[64]:


# Check some statistics for the newly created data frame
rev_gen.describe()


# In[65]:


# Check the value counts (the number of the movies with the same genre)
rev_gen['genres'].value_counts()


# In[66]:


# Extract sub data frame expres the total revenue of each genere and order this data frane desndingly
rev_gen = rev_gen.groupby('genres')['revenue'].sum().reset_index().sort_values(by=['revenue'], ascending=False)


# In[67]:


# Check the newly created data fram
rev_gen


# #### A table shows the rank of the movies' genres based on their portion of the total revenue. It can be noticed that action movies are at the top. 

# In[68]:


# Using area plot to show the highest genere revenue
rev_gen.plot(x='genres', y="revenue", kind="area", figsize=(10, 10), color = 'violet')
plt.legend()
plt.xlabel('The genre')
plt.ylabel('The revenue')
plt.title('The revenue vs the genre')
plt.grid(True)


# #### An area chart visually illustrates the results of the above table. It is easily noted that action and adventure movies are the top two ranks regarding revenue.

# In[69]:


#Convert the column genre as row index for the extracted data frame to prepare for pie chart
rev_gen = rev_gen.set_index('genres')


# In[70]:


# Check the modification performed on the rev_gen data frame
rev_gen


# In[71]:


# Mask for the revenue values over certain limit to just make the chart more clear
rev_gen = rev_gen[rev_gen['revenue'] > 1.852850e+09]


# In[72]:


# Plot a pie chart comparing the contribution for each genre to the revenue
plot = rev_gen.plot.pie(y='revenue', figsize=(15, 15))
plt.title('The total revenue of each movie genre')


# #### A pie chart supports more visual indication about the ranking of movies' genres according to their revenue. It can be noticed that the top four are close to each other.

# ### Research question 5: How is the genres associated to the average voting score? and does this associacion reflect on the revenue?

# In[73]:


# Refer to movie data fram to get columns names
movie.head(0)


# In[74]:


# Extract sub data from from the original one movie data frame
gen_vote = movie[["genres", "vote_count", 'vote_average']]


# In[75]:


# Set criteria taking only the rows for vote count more than 100
gen_vote = gen_vote.query('vote_count > 100')


# In[76]:


# Check 10 rows as a rondom sample from the created data frame
gen_vote.sample(100)


# In[77]:


# Get the overall charchteristics of the created data frame
gen_vote.info()


# In[78]:


# Check the value counts of genre (the total number each genre assigned the movies)
gen_vote.value_counts()


# In[79]:


# Create a list from the sub data frame gen_vote for each genre count
gen_vote_norm = gen_vote.genres.value_counts()


# In[80]:


gen_vote_norm


# In[81]:


# Convert the list to data frame
gen_vote_norm = pd.DataFrame(gen_vote_norm)


# In[82]:


gen_vote_norm


# In[83]:


# Convert the row genre to column
gen_vote_norm.reset_index(level=0, inplace=True)


# In[84]:


# Check if the conversion has been performed
gen_vote_norm


# In[85]:


# Rename the new data fram columns
# Now we should get one column with genres and other for thier counts
gen_vote_norm.rename(columns = {'index':'genres_1', 'genres':'gen_counts'}, inplace = True)


# In[86]:


# Check if the modifications have been performed
gen_vote_norm


# In[87]:


# Create a second data frame represents the total avg vote score per each genre
gen_vote = gen_vote.groupby('genres')['vote_average'].sum().reset_index().sort_values(by=['vote_average'], ascending=False)


# In[88]:


# Check the newly created data frame
gen_vote


# In[89]:


# Convert index of the data frame gen_vote to column as step to reorder the DF
gen_vote = gen_vote.reset_index()


# In[90]:


gen_vote


# In[91]:


# Remove the column named index
gen_vote = gen_vote.drop('index', axis=1)


# In[92]:


# Check the modified data frame
gen_vote


# In[93]:


# Merge gen_vote data frame with gen_vote_norm data frame
gen_vote_comb = gen_vote.merge(gen_vote_norm, left_on='genres', right_on='genres_1', how='inner')


# In[94]:


# Chech the combined data frame has been created as required
gen_vote_comb 


# In[95]:


# DEVIDE COLUMN OF AVG VOTE by GEN COUNTS TO GET THE AVG VOTE SCORE PER GENRE
gen_vote_comb ['vote_avg_per_genre'] = gen_vote_comb['vote_average']/gen_vote_comb ['gen_counts']


# In[96]:


# Check the result of the division process 
gen_vote_comb


# In[97]:


# DELETE UN REQUIRED COLUMNS AS WE NEED TEH RELATION BETWEEN GENRES AND AVG VOTE SCORE PER GENRE
gen_vote_comb.drop(gen_vote_comb.columns[[1,2,3]],axis = 1,inplace=True)
gen_vote_comb


# In[98]:


# Order the DF combined desendingly
gen_vote_comb = gen_vote_comb.sort_values(by=['vote_avg_per_genre'], ascending=False)


# In[99]:


# Check the ordering process has been performed on the combined data frame
gen_vote_comb


# #### A table shows the genres and their corresponding average voting score. It can be noticed that documentary movies have higher scores.

# In[100]:


# Plot horizontal bar chart
gen_vote_comb.plot(x='genres', y="vote_avg_per_genre", kind="barh", figsize=(10, 10), color = 'aqua')
plt.legend()
plt.xlabel('The vote avarege rating per genre')
plt.ylabel('The genre')
plt.title('The genre vas the average vote rating')
plt.grid(True)


# #### A horizontal bar chart visually illustrates the result reached by the above table. It also shows that all genres are very close in the voting score.

# # Research question 6: Does the budget increase has an effect on revenue?

# In[101]:


# Refer to the original data frame movie get the required columns names
movie.head(0)


# In[102]:


# Plot the bar chart for these 2 variables (budget and revenue) to gether 
fig, ax = plt.subplots(figsize =(8,6))
ax.hist(movie['budget'], alpha=0.8, color = 'black', label='budget')
ax.hist(movie['revenue'], alpha=0.6,color = 'orange', label='revenue')
ax.set_title('Distributions of Budget and revenue')
ax.set_xlabel('value of money')
ax.set_ylabel('Count')
ax.legend(loc='upper right')
plt.grid(True)
plt.show();


# #### A bar chart shows the association between the budget and the revenue. A higher budget is associated with higher revenues.

# <a id='conclusions'></a>
# ## Conclusions
# The answers to the research questions are:
# 1. Who are the directors who most direct films?
# 
# Steven Spielberg
# 
# 2. Who are the most actors who have played a starring role in movies?
# 
# Nicolas Cage
# 
# 3. How is the revenue associated with the average voting score?
# 
# We can see that the high revenues are connected to the higher average voting score rating.
# 
# 4. How is the revenue associated with the different genres?
# 
# We can see that action movie have the highest revenues adventures and Drama.
# 
# 5. How are the genres associated with the average voting score? and does this association reflect on the revenue?
# 
# Although we observe that higher revenues are associated with higher average voting score ratings, the genres with high revenues aren't those of higher average voting scores. The highest genre average voting score rating is the documentary.
# This result may refer to the criteria of vote counts exceeds 100 should be increased further example becomes 500
# 
# 6. Does the budget increase affects revenue?
# 
# In most cases, a higher budget is associated with higher revenue. Revenue is multiple higher than budget in most cases. 
# 
# 
# 

# <a id='limitations'></a>
# ## Limitations
# 
# 1. The data set has 6017 revenue values = 0 and 5697 budget fields = 0.
# Accordingly, I removed the rows contain budget or revenue = 0 to get a genuine analysis.
# 
# 2. I set a criteria for all gee analysis that vote_counts must exceeds 100
