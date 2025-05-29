class MyTransformer(TransformerMixin, BaseEstimator):
    '''Шаблон кастомного трансформера'''
 
    def __init__(self):
        '''
        Здесь прописывается инициализация параметров, не зависящих от данных.
        '''
        pass
 
    def fit(self, X, y=None):
        '''
        Здесь прописывается «обучение» трансформера.
        Вычисляются необходимые для работы трансформера параметры (если они нужны).
        '''

        return self
 
    def transform(self, df):
        cols_needed = ['regionName','fullName','ogrn', 'egrulStatus',
       'regionCode',
       'hasRegionalSupport', 'addOkved',
       'statusDetail.shortName','mainOkved.name', 'mainOkved.code',
       'mainOkved.version', 'incomeDetail.grants.totalCount',
       'incomeDetail.grants.totalSum', 'incomeDetail.fedSubsidies.totalCount',
       'incomeDetail.fedSubsidies.totalSum',
       'incomeDetail.contracts44.totalCount',
       'incomeDetail.contracts44.totalSum',
       'incomeDetail.contracts223.totalCount',
       'incomeDetail.contracts223.totalSum',
       'incomeDetail.contracts94.totalCount',
       'incomeDetail.contracts94.totalSum',
       'incomeTotal', 'originDate.$date',
       'dateOgrn.$date', 'dateLiquid.$date',
       'dateReg.$date','minjustForm',
       'okato.code','okato.name',
       'okfs.code','okfs.name',
       'okogu.code','okogu.name',
       'oktmo.code','oktmo.name',
       'opf.code','opf.name']
        df = df[cols_needed]
        df = df.drop(columns=['oktmo.name','okato.name','okogu.name','okato.code','okfs.name','okfs.code','oktmo.code',
                      'okogu.code','minjustForm'])
        df['addOkved'] = df['addOkved'].apply(lambda x: None if isinstance(x,list) and not x else x)
        df = df.drop(columns='addOkved')
        df['contract_count'] = df['incomeDetail.contracts44.totalCount'] + df['incomeDetail.contracts223.totalCount'] + df['incomeDetail.contracts94.totalCount']
        df['contract_sum'] = df['incomeDetail.contracts44.totalSum'] + df['incomeDetail.contracts223.totalSum'] + df['incomeDetail.contracts94.totalSum']
        df = df.drop(columns=['incomeDetail.contracts44.totalCount',
                      'incomeDetail.contracts223.totalCount', 
                      'incomeDetail.contracts94.totalCount', 
                      'incomeDetail.contracts44.totalSum',
                      'incomeDetail.contracts223.totalSum',
                      'incomeDetail.contracts94.totalSum'])
        df['originDate'] = pd.to_datetime(df['originDate.$date'])
        df['dateOgrn'] = pd.to_datetime(df['dateOgrn.$date'])
        df['dateLiquid'] = pd.to_datetime(df['dateLiquid.$date'])
        df['dateReg'] = pd.to_datetime(df['dateReg.$date'])
        df = df.drop(columns=['originDate.$date', 'dateOgrn.$date', 'dateLiquid.$date', 'dateReg.$date'])
        df = df[ ~ ((df['egrulStatus'] == 'Ликвидирована') & (df['dateLiquid'].isnull()))]
        #заменим для удобства типы данных в признаках ogrn и regionCode на числовые
        df['ogrn'] = df['ogrn'].astype('int64')
        df['regionCode'] = df['regionCode'].astype('int64')
        df['hasRegionalSupport'] = df['hasRegionalSupport'].astype('int64') #переведем признак наличия региональной поддержки в бинарный 
        #числовой формат
        df['opf.code'] = df['opf.code'].fillna(0) #отсутствующие opf коды заменим на 0
        df['opf.code'] = df['opf.code'].astype('int64') #такжепереведем признак в числовой формат
        df = df.dropna(subset =['mainOkved.name'])
        df = df.dropna(subset =['regionName'])
        df.loc[df['regionCode'] == 99, 'regionName'] = 'Москва'
        df['regionCode'] = df['regionCode'].apply(lambda x: 77 if x==99 else x)
        df = df.drop(columns=['dateReg'])
        '''
        Здесь прописываются действия с данными.
        '''
        return X