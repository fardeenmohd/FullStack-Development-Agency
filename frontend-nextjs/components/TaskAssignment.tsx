"use client";
import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';

interface Task {
  id: number;
  title: string;
  assignedTo: string;
  status: string;
}

const TaskAssignment: React.FC = () => {
  const dispatch = useDispatch();
  const tasks = useSelector((state: RootState) => state.tasks);
  const [newTask, setNewTask] = useState<Task>({
    id: Date.now(),
    title: '',
    assignedTo: '',
    status: 'pending',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setNewTask(prevState => ({
      ...prevState,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    dispatch({ type: 'ADD_TASK', payload: newTask });
    setNewTask({
      id: Date.now(),
      title: '',
      assignedTo: '',
      status: 'pending',
    });
  };

  return (
    <div className="bg-gray-100 p-8 rounded-lg shadow-md max-w-screen-md mx-auto">
      <h1 className="text-3xl font-bold mb-6">Task Assignment</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="text"
          name="title"
          value={newTask.title}
          onChange={handleInputChange}
          placeholder="Task Title"
          required
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
        />
        <input
          type="text"
          name="assignedTo"
          value={newTask.assignedTo}
          onChange={handleInputChange}
          placeholder="Assigned To"
          required
          className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors duration-200">
          Assign Task
        </button>
      </form>
      <h2 className="text-xl font-semibold mt-8">Tasks</h2>
      <ul className="space-y-4">
        {tasks.map((task) => (
          <li key={task.id} className="bg-white p-4 rounded-lg shadow-md border border-gray-200">
            <div className="flex justify-between items-center">
              <span className="text-xl font-semibold">{task.title}</span>
              <span className="text-gray-500">{task.status}</span>
            </div>
            <p className="mt-2 text-gray-700">Assigned to: {task.assignedTo}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskAssignment;
