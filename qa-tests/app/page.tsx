import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import NotificationManagementDashboard from './app/page';

describe('Notification Management Dashboard', () => {
  it('should allow users to subscribe to different event types', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Subscribe to Events'));
    fireEvent.change(getByRole('textbox'), { target: { value: 'event1' } });
    fireEvent.click(getByText('Add Event'));

    fireEvent.change(getByRole('textbox'), { target: { value: 'event2' } });
    fireEvent.click(getByText('Add Event'));

    await waitFor(() => expect(getByText('event1')).toBeInTheDocument());
    await waitFor(() => expect(getByText('event2')).toBeInTheDocument());
  });

  it('should allow users to configure preferences', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Configure Preferences'));
    fireEvent.change(getByRole('textbox'), { target: { value: 'email' } });
    fireEvent.click(getByText('Save'));

    await waitFor(() => expect(getByText('Email')).toBeInTheDocument());
  });

  it('should receive notifications', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Subscribe to Events'));
    fireEvent.change(getByRole('textbox'), { target: { value: 'event2' } });
    fireEvent.click(getByText('Add Event'));

    // Simulate receiving a notification
    const mockNotification = {
      type: 'email',
      content: 'Event 2 has occurred!'
    };

    handleNotification(mockNotification);

    await waitFor(() => expect(getByText('Event 2 has occurred!')).toBeInTheDocument());
  });

  it('should update in real-time', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Subscribe to Events'));
    fireEvent.change(getByRole('textbox'), { target: { value: 'event3' } });
    fireEvent.click(getByText('Add Event'));

    // Simulate real-time update
    const mockRealTimeUpdate = {
      type: 'email',
      content: 'Event 3 is happening now!'
    };

    handleRealTimeUpdate(mockRealTimeUpdate);

    await waitFor(() => expect(getByText('Event 3 is happening now!')).toBeInTheDocument());
  });

  it('should display error messages for invalid inputs', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Subscribe to Events'));
    fireEvent.change(getByRole('textbox'), { target: { value: '' } });
    fireEvent.click(getByText('Add Event'));

    await waitFor(() => expect(getByText('Please enter a valid event name')).toBeInTheDocument());
  });

  it('should display success messages for successful operations', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Subscribe to Events'));
    fireEvent.change(getByRole('textbox'), { target: { value: 'event4' } });
    fireEvent.click(getByText('Add Event'));

    await waitFor(() => expect(getByText('Event 4 added successfully')).toBeInTheDocument());
  });

  it('should display loading indicators during operations', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Subscribe to Events'));
    fireEvent.change(getByRole('textbox'), { target: { value: 'event5' } });
    fireEvent.click(getByText('Add Event'));

    await waitFor(() => expect(getByText('Loading...')).toBeInTheDocument());
  });

  it('should display error messages for failed operations', async () => {
    const { getByText, getByRole } = render(<NotificationManagementDashboard />);

    fireEvent.click(getByText('Subscribe to Events'));
    fireEvent.change(getByRole('textbox'), { target: { value: 'event6' } });
    fireEvent.click(getByText('Add Event'));

    // Simulate a failed operation
    const mockFailedOperation = {
      type: 'error',
      content: 'Failed to add event'
    };

    handleFailedOperation(mockFailedOperation);

    await waitFor(() => expect(getByText('Failed to add event')).toBeInTheDocument());
  });
});
