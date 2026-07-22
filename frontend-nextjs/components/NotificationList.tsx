import React from 'react';

interface Notification {
  id: number;
  milestoneType: string;
  timestamp: Date;
  method: string;
}

const NotificationItem: React.FC<{ notification: Notification }> = ({ notification }) => (
  <li key={notification.id}>
    <strong>{notification.milestoneType}</strong> - {notification.timestamp.toLocaleString()} via {notification.method}
  </li>
);

const NotificationList: React.FC<{ notifications: Notification[] }> = ({ notifications }) => (
  <ul>
    {notifications.map(notification => (
      <NotificationItem notification={notification} />
    ))}
  </ul>
);

export default NotificationList;
