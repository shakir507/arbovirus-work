def priors_history(nParams, nsd):
    piece_directory =  OUTPUT_DIR + "piece_"+str(nsd-1) + "/"
    #parameters_ran = [0] * nParams * 2
    parameters_ran = [0] * nParams

    rmse_save_posterior(parameters_ran, piece_directory, nsd-1)
    rmse_table = pd.read_csv(os.path.join(piece_directory,"rmse_priors_"+str(nsd-1)+".csv"))

    chicrit=stats.chi2.ppf(1-0.05, df=NUM_DAYS)
    print(chicrit)
    posterior_index=[]

# use big number for saving all/// relax conditions
    # for i in rmse_table['index']:
    #     if rmse_table['RMSE'][i] < chicrit and rmse_table['RMSE'][i]>0:
    #         posterior_index.append(i)
    # if len(posterior_index)==0: # make sure... posterior is not empty
    #     posterior_index=list(rmse_table.index.values)

    # Fix this: RMSE condition need to be relaxed to get enough parameter sets from prior
    # MIN_NUM_index=20
    # RMSE_THRESHOLD=1000

    MIN_NUM_index=20
    RMSE_THRESHOLD=1000000
    r_th=10
    while(len(list(set(posterior_index)))<MIN_NUM_index and r_th<RMSE_THRESHOLD): # sk & Shakir (10/20): relax conditions based on total # of simulations per 30 days
        for i in rmse_table['index']:
            if rmse_table['RMSE'][i]<r_th and rmse_table['RMSE'][i]>0:
                posterior_index.append(i)
        r_th+=1

    posterior_index=list(set(posterior_index))
    prior=pd.read_csv(os.path.join(piece_directory,"prior_parameters_sequential_"+str(nsd-1)+".csv"))
    posterior0=prior.iloc[posterior_index]
    infectedcases=[]
    for jk in posterior_index:
        output_directory =  piece_directory + str(int(jk)) + "/"
        START_DAY = (nsd-1) * NUM_DAYS
        filename="infections_from_new_strain"+str(START_DAY)+"_"+str(NUM_DAYS)+".csv"
        if(os.path.exists(filename)):
            inf=pd.read_csv(filename)
            infectedcases.append(inf['total_new_infections'][len(inf)-1])
    # sk 10/20
    minValues['INIT_FIXED_NUMBER_INFECTED']=min(infectedcases+[1]);
    maxValues['INIT_FIXED_NUMBER_INFECTED']=max(infectedcases+[1]);
#------------------Beta: home, school, work, community------------------------#
    minValues['BETA_SCALE']=min(posterior0['BETA_SCALE']);
    maxValues['BETA_SCALE']=max(posterior0['BETA_SCALE']);
    
    minValues['BETA_H']=min(posterior0['BETA_H'])#0.0001;
    maxValues['BETA_H']=max(posterior0['BETA_H']);#9
    
    minValues['BETA_PROJECT']=min(posterior0['BETA_PROJECT']);
    maxValues['BETA_PROJECT']=max(posterior0['BETA_PROJECT']);
    
    minValues['BETA_NBR_CELLS']=min(posterior0['BETA_NBR_CELLS']);
    maxValues['BETA_NBR_CELLS']=max(posterior0['BETA_NBR_CELLS']);
    
    minValues['BETA_CLASS']=min(posterior0['BETA_CLASS']);
    maxValues['BETA_CLASS']=max(posterior0['BETA_CLASS']);
    
    minValues['BETA_TRAVEL']=min(posterior0['BETA_TRAVEL']);
    maxValues['BETA_TRAVEL']=max(posterior0['BETA_TRAVEL']);
#-----------------------------------------------------------------------------#
    #priors(nParams)
    rangeParam={}
    for ld in minValues:
        rangeParam[ld]=maxValues[ld]-minValues[ld]
#-----------------------------------------------------------------------------#

    paraLHS=lhs(len(minValues), samples=nParams, criterion='corr');#to use the correlation feature, the dimension of the matrix should be more than 1.
    
#-----------------------------------------------------------------------------#
    i=0;
    VarParamsLHS=pd.DataFrame()
    for ld in minValues:
        VarParamsLHS[ld]=minValues[ld]+rangeParam[ld]*paraLHS[:,i]
        i=i+1

    # VarParamsLHS['PROVIDE_INITIAL_SEED_GRAPH']=random.sample(range(1, nParams+1), nParams) # Change
    # VarParamsLHS['PROVIDE_INITIAL_SEED']=random.sample(range(1, nParams+1), nParams) # Change
    VarParamsLHS['PROVIDE_INITIAL_SEED_GRAPH']=7
    VarParamsLHS['PROVIDE_INITIAL_SEED']=1
    return VarParamsLHS