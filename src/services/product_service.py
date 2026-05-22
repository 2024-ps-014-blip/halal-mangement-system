#!/usr/bin/env python3

"""
Product Service

Business logic for product management.
"""

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from config.database import db
from models.product import Product
from config.settings import logger

class ProductService:
    """
    Service class for product operations.
    """
    
    @staticmethod
    def create_product(product_data):
        """
        Create a new product.
        
        Args:
            product_data: Dictionary with product information
            
        Returns:
            Created product object
        """
        try:
            session = db.get_session()
            product = Product(**product_data)
            session.add(product)
            session.commit()
            logger.info(f"Product created: {product.id} - {product.name}")
            return product
        except IntegrityError as e:
            session.rollback()
            logger.error(f"Product creation error (duplicate): {str(e)}")
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"Product creation error: {str(e)}")
            raise
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_product(product_id):
        """
        Get product by ID.
        
        Args:
            product_id: Product identifier
            
        Returns:
            Product object or None
        """
        try:
            session = db.get_session()
            product = session.query(Product).filter(Product.id == product_id).first()
            return product
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_all_products(page=1, per_page=20):
        """
        Get all products with pagination.
        
        Args:
            page: Page number
            per_page: Items per page
            
        Returns:
            List of products and total count
        """
        try:
            session = db.get_session()
            query = session.query(Product).order_by(Product.created_at.desc())
            total = query.count()
            products = query.offset((page - 1) * per_page).limit(per_page).all()
            return products, total
        finally:
            db.close_session(session)
    
    @staticmethod
    def update_product(product_id, product_data):
        """
        Update product information.
        
        Args:
            product_id: Product identifier
            product_data: Dictionary with updated information
            
        Returns:
            Updated product object
        """
        try:
            session = db.get_session()
            product = session.query(Product).filter(Product.id == product_id).first()
            if not product:
                return None
            
            for key, value in product_data.items():
                if hasattr(product, key) and key != 'id':
                    setattr(product, key, value)
            
            product.updated_at = datetime.utcnow()
            session.commit()
            logger.info(f"Product updated: {product_id}")
            return product
        except Exception as e:
            session.rollback()
            logger.error(f"Product update error: {str(e)}")
            raise
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_certified_products():
        """
        Get all halal-certified products.
        
        Returns:
            List of certified products
        """
        try:
            session = db.get_session()
            products = session.query(Product).filter(
                Product.is_halal_certified == True,
                Product.status == 'active'
            ).all()
            return products
        finally:
            db.close_session(session)
    
    @staticmethod
    def get_expiring_certifications(days=30):
        """
        Get products with certifications expiring soon.
        
        Args:
            days: Number of days to check ahead
            
        Returns:
            List of products with expiring certifications
        """
        try:
            session = db.get_session()
            expiry_threshold = datetime.utcnow() + timedelta(days=days)
            products = session.query(Product).filter(
                Product.certification_expiry <= expiry_threshold,
                Product.certification_expiry >= datetime.utcnow(),
                Product.is_halal_certified == True
            ).all()
            return products
        finally:
            db.close_session(session)
