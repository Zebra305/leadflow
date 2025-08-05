from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Lead
from datetime import datetime, timedelta
from sqlalchemy import or_, and_

@app.route('/')
def dashboard():
    """Main dashboard showing leads ready for outreach"""
    # Get leads that are ready for next message (2-day rule)
    ready_leads = []
    all_leads = Lead.query.all()
    
    for lead in all_leads:
        message, msg_type, suffix = lead.get_current_message_info()
        if message and lead.is_ready_for_next_message():
            ready_leads.append({
                'lead': lead,
                'message': message,
                'message_type': msg_type,
                'suffix': suffix
            })
    
    # Get waiting leads (not ready due to 2-day rule)
    waiting_leads = []
    for lead in all_leads:
        message, msg_type, suffix = lead.get_current_message_info()
        if message and not lead.is_ready_for_next_message():
            next_available = lead.get_next_available_time()
            hours_left = int((next_available - datetime.utcnow()).total_seconds() / 3600)
            waiting_leads.append({
                'lead': lead,
                'message_type': msg_type,
                'hours_left': max(0, hours_left)
            })
    
    return render_template('dashboard.html', 
                         ready_leads=ready_leads, 
                         waiting_leads=waiting_leads)

@app.route('/search')
def search():
    """Search leads interface"""
    query = request.args.get('q', '')
    results = []
    
    if query:
        # Search across multiple fields
        search_conditions = [
            Lead.email.ilike(f'%{query}%'),
            Lead.website.ilike(f'%{query}%'),
            Lead.telegram.ilike(f'%{query}%')
        ]
        
        if query.isdigit():
            search_conditions.append(Lead.id == int(query))
            
        search_filter = or_(*search_conditions)
        results = Lead.query.filter(search_filter).all()
    
    return render_template('search.html', query=query, results=results)

@app.route('/lead/<int:lead_id>')
def lead_detail(lead_id):
    """Detailed view of a specific lead"""
    lead = Lead.query.get_or_404(lead_id)
    message, msg_type, suffix = lead.get_current_message_info()
    
    # Get message history
    message_history = []
    
    # Add outreach to history
    if lead.outreach:
        message_history.append({
            'type': 'Initial Outreach',
            'message': lead.outreach,
            'sent': lead.sent,
            'replied': lead.replied,
            'suffix': ''
        })
    
    # Add follow-ups to history
    follow_ups = [
        ('Follow-up 1', lead.follow_up_0, lead.sent_0, lead.replied_0, '_0'),
        ('Follow-up 2', lead.follow_up_1, lead.sent_1, lead.replied_1, '_1'),
        ('Follow-up 3', lead.follow_up_2, lead.sent_2, lead.replied_2, '_2'),
        ('Follow-up 4', lead.follow_up_3, lead.sent_3, lead.replied_3, '_3'),
        ('Follow-up 5', lead.follow_up_4, lead.sent_4, lead.replied_4, '_4'),
        ('Follow-up 6', lead.follow_up_5, lead.sent_5, lead.replied_5, '_5'),
    ]
    
    for msg_type_hist, message_text, sent, replied, suffix_hist in follow_ups:
        if message_text:
            message_history.append({
                'type': msg_type_hist,
                'message': message_text,
                'sent': sent,
                'replied': replied,
                'suffix': suffix_hist
            })
    
    return render_template('lead_detail.html', 
                         lead=lead, 
                         current_message=message,
                         current_message_type=msg_type,
                         current_suffix=suffix,
                         message_history=message_history,
                         is_ready=lead.is_ready_for_next_message(),
                         next_available=lead.get_next_available_time())

@app.route('/mark_sent/<int:lead_id>/<suffix>')
def mark_sent(lead_id, suffix):
    """Mark a message as sent"""
    lead = Lead.query.get_or_404(lead_id)
    
    try:
        # Update the appropriate sent field
        if suffix == '':
            lead.sent = True
        else:
            setattr(lead, f'sent{suffix}', True)
        
        # Update timestamp
        lead.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Message marked as sent for {lead.email or lead.website or f"Lead {lead.id}"}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating lead: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/mark_replied/<int:lead_id>/<suffix>')
def mark_replied(lead_id, suffix):
    """Mark a message as replied"""
    lead = Lead.query.get_or_404(lead_id)
    
    try:
        # Update the appropriate replied field
        if suffix == '':
            lead.replied = True
        else:
            setattr(lead, f'replied{suffix}', True)
        
        # Update timestamp
        lead.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'Message marked as replied for {lead.email or lead.website or f"Lead {lead.id}"}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating lead: {str(e)}', 'error')
    
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/stats')
def stats():
    """Show campaign statistics"""
    total_leads = Lead.query.count()
    
    # Count sent messages
    sent_outreach = Lead.query.filter(Lead.sent == True).count()
    sent_followups = sum([
        Lead.query.filter(getattr(Lead, f'sent_{i}') == True).count()
        for i in range(6)
    ])
    
    # Count replied messages
    replied_outreach = Lead.query.filter(Lead.replied == True).count()
    replied_followups = sum([
        Lead.query.filter(getattr(Lead, f'replied_{i}') == True).count()
        for i in range(6)
    ])
    
    return render_template('stats.html',
                         total_leads=total_leads,
                         sent_outreach=sent_outreach,
                         sent_followups=sent_followups,
                         replied_outreach=replied_outreach,
                         replied_followups=replied_followups)
