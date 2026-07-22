"use client";
import React, { useState } from 'react';

interface NotificationFormProps {
  onSubmit: (milestoneType: string, notificationMethod: string) => void;
}

const NotificationForm: React.FC<NotificationFormProps> = ({ onSubmit }) => {
  const [milestoneType, setMilestoneType] = useState('');
  const [notificationMethod, setNotificationMethod] = useState('');

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(milestoneType, notificationMethod);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="milestoneType">Milestone Type:</label>
        <input
          type="text"
          id="milestoneType"
          value={milestoneType}
          onChange={(e) => setMilestoneType(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="notificationMethod">Notification Method:</label>
        <select
          id="notificationMethod"
          value={notificationMethod}
          onChange={(e) => setNotificationMethod(e.target.value)}
          required
        >
          <option value="">Select a method</option>
          <option value="email">Email</option>
          <option value="sms">SMS</option>
          <option value="push">Push Notification</option>
        </select>
      </div>
      <button type="submit">Submit</button>
    </form>
  );
};

export default NotificationForm;
