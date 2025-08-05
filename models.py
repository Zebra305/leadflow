from app import db
from datetime import datetime
from sqlalchemy import text

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    raw_html = db.Column(db.Text)
    image_to_text = db.Column(db.Text)
    telegram = db.Column(db.String(255))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    
    # Outreach sequence
    outreach = db.Column(db.Text)
    sent = db.Column(db.Boolean, default=False)
    replied = db.Column(db.Boolean, default=False)
    
    # Follow-ups 0-5
    follow_up_0 = db.Column(db.Text)
    sent_0 = db.Column(db.Boolean, default=False)
    replied_0 = db.Column(db.Boolean, default=False)
    
    follow_up_1 = db.Column(db.Text)
    sent_1 = db.Column(db.Boolean, default=False)
    replied_1 = db.Column(db.Boolean, default=False)
    
    follow_up_2 = db.Column(db.Text)
    sent_2 = db.Column(db.Boolean, default=False)
    replied_2 = db.Column(db.Boolean, default=False)
    
    follow_up_3 = db.Column(db.Text)
    sent_3 = db.Column(db.Boolean, default=False)
    replied_3 = db.Column(db.Boolean, default=False)
    
    follow_up_4 = db.Column(db.Text)
    sent_4 = db.Column(db.Boolean, default=False)
    replied_4 = db.Column(db.Boolean, default=False)
    
    follow_up_5 = db.Column(db.Text)
    sent_5 = db.Column(db.Boolean, default=False)
    replied_5 = db.Column(db.Boolean, default=False)
    
    # Additional fields
    free_demo = db.Column(db.Boolean, default=False)
    meeting = db.Column(db.Boolean, default=False)
    money_in = db.Column(db.Boolean, default=False)
    extracted_text_from_image = db.Column(db.Text)
    processed_main = db.Column(db.Text)
    processed_text = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(255))
    last_modified_by = db.Column(db.String(255))
    
    # Additional fields
    SWOT = db.Column(db.Text)
    ExtractionAgent = db.Column(db.Text)
    
    def get_current_message_info(self):
        """
        Returns the current message to send and its status.
        Returns (message_text, message_type, field_prefix) or (None, None, None) if all sent or replied
        """
        # Check outreach first
        if not self.sent and self.outreach:
            return (self.outreach, "Initial Outreach", "")
        elif self.replied:
            return (None, "Replied", "")
        
        # Check follow-ups in order
        follow_ups = [
            (self.follow_up_0, self.sent_0, self.replied_0, "Follow-up 1", "_0"),
            (self.follow_up_1, self.sent_1, self.replied_1, "Follow-up 2", "_1"),
            (self.follow_up_2, self.sent_2, self.replied_2, "Follow-up 3", "_2"),
            (self.follow_up_3, self.sent_3, self.replied_3, "Follow-up 4", "_3"),
            (self.follow_up_4, self.sent_4, self.replied_4, "Follow-up 5", "_4"),
            (self.follow_up_5, self.sent_5, self.replied_5, "Follow-up 6", "_5"),
        ]
        
        for message, sent, replied, msg_type, suffix in follow_ups:
            if replied:
                return (None, "Replied", suffix)
            if not sent and message:
                return (message, msg_type, suffix)
        
        return (None, "All Messages Sent", "")
    
    def is_ready_for_next_message(self):
        """
        Check if enough time (2 days) has passed since last message was sent
        """
        if not self.updated_at:
            return True
        
        from datetime import datetime, timedelta
        two_days_ago = datetime.utcnow() - timedelta(days=2)
        return self.updated_at <= two_days_ago
    
    def get_last_sent_timestamp(self):
        """Get the timestamp of when the last message was sent"""
        # This would be the updated_at field when a message was marked as sent
        return self.updated_at
    
    def get_next_available_time(self):
        """Get when the next message can be sent (2 days after last sent)"""
        if not self.updated_at:
            return datetime.utcnow()
        
        from datetime import timedelta
        return self.updated_at + timedelta(days=2)
