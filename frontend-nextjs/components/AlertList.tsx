import React from 'react';
import { Alert } from './Alert';

interface Alert {
  id: number;
  message: string;
}

interface AlertListProps {
  alerts: Alert[];
  onEdit: (alertId: number) => void;
  onDelete: (alertId: number) => void;
}

const AlertList: React.FC<AlertListProps> = ({ alerts, onEdit, onDelete }) => (
  <ul>
    {alerts.map(alert => (
      <li key={alert.id}>
        <Alert message={alert.message} />
        <button onClick={() => handleAction(onEdit, alert.id)}>Edit</button>
        <button onClick={() => handleAction(onDelete, alert.id)}>Delete</button>
      </li>
    ))}
  </ul>
);

const handleAction = (action: (id: number) => void, id: number) => {
  action(id);
};

export default AlertList;
