from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData
from sqlalchemy.orm import sessionmaker

class LeadScoringService:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
        self.leads_table = Table('leads', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String),
            Column('email', String),
            Column('phone', String),
            Column('source', String),
            Column('status', String),
            Column('score', Float)
        )

    def fetch_leads(self):
        session = self.Session()
        query = self.leads_table.select()
        result = session.execute(query).fetchall()
        session.close()
        return result

    def calculate_scores(self, leads):
        for lead in leads:
            score = 0
            if 'email' in lead and '@' in lead['email']:
                score += 1
            if 'phone' in lead and len(lead['phone']) == 10:
                score += 1
            if 'source' in lead and lead['source'] == 'organic':
                score += 2
            lead['score'] = score
        return leads

    def calculate_conversion_rates(self, leads):
        converted_leads = [lead for lead in leads if lead['status'] == 'converted']
        conversion_rate = len(converted_leads) / len(leads) if leads else 0
        return conversion_rate

    def calculate_compliance_risks(self, leads):
        risky_leads = [lead for lead in leads if not self.is_email_valid(lead)]
        compliance_risk = len(risky_leads) / len(leads) if leads else 0
        return compliance_risk

    def is_email_valid(self, lead):
        return 'email' in lead and '@' in lead['email']

    def update_lead_scores(self):
        leads = self.fetch_leads()
        updated_leads = self.calculate_scores(leads)
        session = self.Session()
        for lead in updated_leads:
            query = self.leads_table.update().where(self.leads_table.c.id == lead['id']).values(score=lead['score'])
            session.execute(query)
        session.commit()
        session.close()

    def get_real_time_data(self):
        leads = self.fetch_leads()
        scores = [lead['score'] for lead in leads]
        conversion_rate = self.calculate_conversion_rates(leads)
        compliance_risk = self.calculate_compliance_risks(leads)
        return {
            'scores': scores,
            'conversion_rate': conversion_rate,
            'compliance_risk': compliance_risk
        }
