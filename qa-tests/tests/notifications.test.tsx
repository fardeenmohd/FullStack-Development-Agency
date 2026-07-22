import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import Notifications from '../Notifications';

describe('Notifications', () => {
  it('should subscribe to an event and receive a notification', async () => {
    const mockEvent = 'newMessage';
    const mockNotification = 'New message received!';

    const handleNotification = jest.fn();
    render(<Notifications onEvent={mockEvent} onNotify={handleNotification} />);

    fireEvent.click(screen.getByText('Subscribe to New Messages'));
    expect(handleNotification).toHaveBeenCalledWith(mockNotification);
  });

  it('should configure preferences and send notifications based on preferences', async () => {
    const mockEvent = 'newMessage';
    const mockNotification = 'New message received!';
    const mockPreferences = { frequency: 'daily' };

    const handleNotification = jest.fn();
    render(<Notifications onEvent={mockEvent} onNotify={handleNotification} preferences={mockPreferences} />);

    fireEvent.click(screen.getByText('Subscribe to New Messages'));
    expect(handleNotification).toHaveBeenCalledWith(mockNotification);
  });

  it('should not send notifications if preferences are set to none', async () => {
    const mockEvent = 'newMessage';
    const mockNotification = 'New message received!';
    const mockPreferences = { frequency: 'none' };

    const handleNotification = jest.fn();
    render(<Notifications onEvent={mockEvent} onNotify={handleNotification} preferences={mockPreferences} />);

    fireEvent.click(screen.getByText('Subscribe to New Messages'));
    expect(handleNotification).not.toHaveBeenCalledWith(mockNotification);
  });

  it('should store subscriptions correctly in the database', async () => {
    const mockEvent = 'newMessage';
    const mockUser = { id: 1, email: 'user@example.com' };

    render(<Notifications onEvent={mockEvent} user={mockUser} />);

    fireEvent.click(screen.getByText('Subscribe to New Messages'));
    // Add assertions to check if subscription is stored in the database
  });

  it('should send notifications as expected when events occur', async () => {
    const mockEvent = 'newMessage';
    const mockNotification = 'New message received!';
    const mockUser = { id: 1, email: 'user@example.com' };

    render(<Notifications onEvent={mockEvent} onNotify={() => console.log(mockNotification)} user={mockUser} />);

    fireEvent.click(screen.getByText('Subscribe to New Messages'));
    // Add assertions to check if notification is sent
  });
});
