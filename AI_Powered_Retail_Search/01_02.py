import json
from datetime import datetime, timedelta

def shift_dates_to_today(input_file, output_file):
    """
    Uniformly shift all event dates so the latest date matches today's date.
    
    This preserves the relative time distribution of events while making
    the data current. All dates move by the same number of days.
    
    Args:
        input_file (str): Path to the input JSONL file with events
        output_file (str): Path to save the date-shifted JSONL file
    """
    try:
        print("=== SHIFTING EVENT DATES TO TODAY ===")
        
        # Set target date (default to today at 23:59:59)
        target_date = datetime(2026, 11, 20, 16, 40, 59)
        
        print(f"🎯 Target latest date: {target_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load all events
        print(f"\n📖 Loading events from {input_file}...")
        events = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    event = json.loads(line.strip())
                    events.append(event)
                except json.JSONDecodeError as e:
                    print(f"⚠️  Error parsing line {line_num}: {e}")
                    continue
        
        print(f"✅ Loaded {len(events):,} events")
        
        # Find current date range
        print(f"\n🔍 Analyzing current date range...")
        event_dates = []
        for event in events:
            if 'eventTime' in event:
                try:
                    # Parse the ISO format timestamp
                    time_str = event['eventTime'].replace('Z', '').split('.')[0]
                    event_dt = datetime.fromisoformat(time_str)
                    event_dates.append(event_dt)
                except (ValueError, AttributeError) as e:
                    print(f"⚠️  Could not parse eventTime: {event.get('eventTime')}")
                    continue
        
        if not event_dates:
            print("❌ ERROR: No valid event dates found!")
            return
        
        # Calculate current date range
        min_date = min(event_dates)
        max_date = max(event_dates)
        date_range_days = (max_date - min_date).days
        
        print(f"📅 Current date range:")
        print(f"   Oldest event: {min_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Latest event: {max_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Range: {date_range_days} days")
        
        # Calculate the time shift needed
        time_shift = target_date - max_date
        days_shift = time_shift.days
        print(f"\n⏰ Time shift needed: {days_shift:+d} days")
        
        # Calculate new date range
        new_min_date = min_date + time_shift
        new_max_date = max_date + time_shift
        
        print(f"\n📅 New date range after shift:")
        print(f"   Oldest event: {new_min_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Latest event: {new_max_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Range: {date_range_days} days (preserved)")
        
        # Apply the shift to all events
        print(f"\n🔄 Shifting all event dates by {days_shift:+d} days...")
        shifted_events = []
        events_shifted = 0
        
        for event in events:
            if 'eventTime' in event:
                try:
                    # Parse the timestamp
                    time_str = event['eventTime'].replace('Z', '').split('.')[0]
                    event_dt = datetime.fromisoformat(time_str)
                    
                    # Apply the shift
                    shifted_dt = event_dt + time_shift
                    
                    # Format back to ISO format with Z suffix
                    event['eventTime'] = shifted_dt.strftime('%Y-%m-%dT%H:%M:%S.000Z')
                    events_shifted += 1
                    
                except (ValueError, AttributeError):
                    # Keep original if parsing fails
                    pass
            
            shifted_events.append(event)
            
            if (events_shifted) % 10000 == 0:
                print(f"   Shifted {events_shifted:,} events...")
        
        # Write shifted events to output file
        print(f"\n💾 Writing shifted events to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            for event in shifted_events:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        print(f"\n=== DATE SHIFT COMPLETE ===")
        print(f"✅ Input: {input_file}")
        print(f"✅ Output: {output_file}")
        print(f"✅ Total events: {len(shifted_events):,}")
        print(f"✅ Events with dates shifted: {events_shifted:,}")
        print(f"⏰ Time shift applied: {days_shift:+d} days")
        
        # Show sample shifted events
        print(f"\n=== SAMPLE SHIFTED EVENTS ===")
        for i in range(min(3, len(shifted_events))):
            event = shifted_events[i]
            print(f"\nEvent {i+1}:")
            print(f"   Type: {event.get('eventType', 'N/A')}")
            print(f"   Time: {event.get('eventTime', 'N/A')}")
            print(f"   Visitor: {event.get('visitorId', 'N/A')}")
        
        # Count event types
        event_type_counts = {}
        for event in shifted_events:
            event_type = event.get('eventType', 'unknown')
            event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
        
        print(f"\n📊 Event Type Distribution:")
        for event_type, count in sorted(event_type_counts.items()):
            print(f"   - {event_type}: {count:,} events")
        
        print(f"\n🎯 SUCCESS!")
        print(f"📋 All event dates have been uniformly shifted")
        print(f"   ✅ Latest date is now: {target_date.strftime('%Y-%m-%d')}")
        print(f"   ✅ Relative time distribution preserved")
        print(f"   ✅ Ready for Vertex AI Search for Commerce import")
        
        return shifted_events, time_shift
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function to shift event dates to today."""
    input_file = 'user_events.jsonl'
    output_file = 'user_events_current_dates.jsonl'

    
    print("🚀 Shifting Event Dates to Today")
    print("   Moving all event dates uniformly to make data current")
    
    try:
        events, shift = shift_dates_to_today(input_file, output_file)
        print(f"\n✨ COMPLETE!")
        print(f"   Shifted {len(events):,} events by {shift.days:+d} days")
        print(f"   Use {output_file} for current date-based analysis")
        
    except Exception as e:
        print(f"\n❌ FAILED!")
        print(f"   Error: {e}")

if __name__ == "__main__":
    main()

