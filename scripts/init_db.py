import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.core.database import engine
from app.models.data_models.document import Document
from app.models.data_models.user import User
from app.models.data_models.session import UserSession
from app.models.data_models.subscription import Subscription
from app.models.data_models.billing_address import BillingAddress
from app.models.data_models.pageviews import PageView
from app.models.data_models.funnel import ConversionFunnel
from app.models.data_models.userevents import UserEvent
from app.core.database import Base


if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
