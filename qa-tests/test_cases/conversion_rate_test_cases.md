# conversion_rate_test_cases.py

def calculate_conversion_rate(total_leads, converted_leads):
    """
    Calculate the conversion rate based on total leads and converted leads.
    
    Args:
        total_leads (int): Total number of leads.
        converted_leads (int): Number of converted leads.
        
    Returns:
        float: Conversion rate as a percentage.
        
    Raises:
        ValueError: If total_leads or converted_leads are negative, non-integer, or non-numeric.
    """
    if not isinstance(total_leads, int) or not isinstance(converted_leads, int):
        raise ValueError("Total leads and converted leads must be integers.")
    
    if total_leads < 0 or converted_leads < 0:
        raise ValueError("Total leads and converted leads cannot be negative.")
    
    if total_leads == 0:
        raise ValueError("Total leads cannot be zero when calculating conversion rate.")
    
    return (converted_leads / total_leads) * 100

def test_conversion_rate():
    assert calculate_conversion_rate(100, 20) == 20.0
    assert calculate_conversion_rate(500, 450) == 90.0
    assert calculate_conversion_rate(200, 10) == 5.0
    assert calculate_conversion_rate(300, 0) == 0.0
    assert calculate_conversion_rate(1_000_000, 250_000) == 25.0

def test_negative_values():
    try:
        calculate_conversion_rate(-50, 10)
    except ValueError as e:
        assert str(e) == "Total leads and converted leads cannot be negative."
    
    try:
        calculate_conversion_rate(100, -5)
    except ValueError as e:
        assert str(e) == "Total leads and converted leads cannot be negative."

def test_non_integer_values():
    try:
        calculate_conversion_rate(120.5, 24)
    except ValueError as e:
        assert str(e) == "Total leads and converted leads must be integers."
    
    try:
        calculate_conversion_rate("100", "20")
    except ValueError as e:
        assert str(e) == "Total leads and converted leads must be integers."

def test_zero_denominator():
    try:
        calculate_conversion_rate(0, 10)
    except ValueError as e:
        assert str(e) == "Total leads cannot be zero when calculating conversion rate."

def test_multiple_periods():
    assert calculate_conversion_rate(100, 20) == 20.0
    assert calculate_conversion_rate(150, 30) == 20.0

def test_deletion_of_data():
    # Assuming initial data is stored and can be deleted
    pass

def test_update_of_data():
    # Assuming initial data is stored and can be updated
    pass

def test_missing_data():
    # Assuming initial data is stored and some periods may be missing
    pass

def test_large_dataset():
    assert calculate_conversion_rate(1_000_000, 250_000) == 25.0

def test_zero_total_leads_with_converted_leads():
    try:
        calculate_conversion_rate(0, 5)
    except ValueError as e:
        assert str(e) == "Total leads cannot be zero when calculating conversion rate."

def test_zero_converted_leads_with_total_leads():
    assert calculate_conversion_rate(100, 0) == 0.0

def test_decimal_places():
    assert calculate_conversion_rate(250, 64) == 25.6

def test_rounding():
    assert round(calculate_conversion_rate(300, 78), 2) == 26.0

def test_large_rounding_errors():
    assert calculate_conversion_rate(1_000_000, 999_999) == 99.99
