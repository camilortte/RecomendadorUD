from recsys.algorithm.factorize import SVD
svd = SVD()
svd.load_data(filename='/home/camilortte/Desktop/Recommender/ml-100k/movies.csv',
            sep=',',
            format={'col':0, 'row':1, 'value':2, 'ids': int})
k = 100
svd.compute(k=k,
            min_values=0,
            pre_normalize=None,
            mean_center=True,
            post_normalize=True,
            savefile='/home/camilortte/Desktop/Recommender/ml-100k/movies-temp.csv')

svd.recommend(1, is_row=False) #cols are users and rows are items, thus we set is_row=False
