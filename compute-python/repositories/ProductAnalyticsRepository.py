from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class AnalyticsData(Base):
    __tablename__ = 'analytics_data'
    id = Column(Integer, primary_key=True)
    product_id = Column(String)
    date = Column(Date)
    sales = Column(Float)
    views = Column(Float)

class ProductAnalyticsRepository:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def fetch_analytics_by_product_id(self, product_id):
        return self.session.query(AnalyticsData).filter_by(product_id=product_id).all()

    def store_analytics_data(self, data):
        for item in data:
            analytics_item = AnalyticsData(
                product_id=item['product_id'],
                date=item['date'],
                sales=item['sales'],
                views=item['views']
            )
            self.session.add(analytics_item)
        self.session.commit()
