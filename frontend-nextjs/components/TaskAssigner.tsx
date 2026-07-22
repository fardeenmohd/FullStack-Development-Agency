"use client";
import React, { useState } from 'react';

interface Task {
  id: number;
  description: string;
  status: string;
  assignedTo: string | null;
}

const TaskAssigner: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, description: 'Update product page', status: 'pending', assignedTo: null },
    { id: 2, description: 'Fix bug in checkout process', status: 'in progress', assignedTo: 'John' },
    { id: 3, description: 'Add new feature to app', status: 'completed', assignedTo: 'Jane' }
  ]);
  const [teamMembers, setTeamMembers] = useState<string[]>(['John', 'Jane', 'Alice']);

  const handleAssignTask = (taskId: number, member: string) => {
    setTasks(tasks.map(task => 
      task.id === taskId ? { ...task, assignedTo: member } : task
    ));
  };

  const handleStatusChange = (taskId: number, status: string) => {
    setTasks(tasks.map(task => 
      task.id === taskId ? { ...task, status } : task
    ));
  };

  return (
    <div>
      {tasks.map(task => (
        <div key={task.id}>
          <p>{task.description}</p>
          <select value={task.assignedTo || ''} onChange={(e) => handleAssignTask(task.id, e.target.value)}>
            <option value="">Select a team member</option>
            {teamMembers.map(member => (
              <option key={member} value={member}>{member}</option>
            ))}
          </select>
          <select value={task.status} onChange={(e) => handleStatusChange(task.id, e.target.value)}>
            <option value="pending">Pending</option>
            <option value="in progress">In Progress</option>
            <option value="completed">Completed</option>
          </select>
        </div>
      ))}
    </div>
  );
};

export default TaskAssigner;
