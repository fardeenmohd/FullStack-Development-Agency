import React from 'react';
import { Task } from '../types/Task';

interface TaskListProps {
  tasks: Task[];
}

const TaskList: React.FC<TaskListProps> = ({ tasks }) => {
  return (
    <ul className="divide-y divide-gray-200">
      {tasks.map((task) => (
        <li key={task.id} className="py-4 px-4 sm:px-6 lg:px-8">
          <div className="flex items-center space-x-3">
            <div className="min-w-0 flex-1">
              <p className="text-sm font-medium text-gray-900 truncate">{task.title}</p>
              <p className="mt-2 text-xs text-gray-500 truncate">
                Status: {task.status} - Completed on: {task.completedAt}
              </p>
            </div>
          </div>
        </li>
      ))}
    </ul>
  );
};

export default TaskList;
