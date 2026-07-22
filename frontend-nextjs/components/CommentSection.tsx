"use client";
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

interface Comment {
  id: number;
  text: string;
}

const CommentSection: React.FC<{ initialComments: Comment[] }> = ({ initialComments }) => {
  const [comments, setComments] = useState<Comment[]>(initialComments);
  const [newComment, setNewComment] = useState<string>('');
  const [editingId, setEditingId] = useState<number | null>(null);

  useEffect(() => {
    const socket = io('http://localhost:3001'); // Replace with your WebSocket server URL

    socket.on('commentAdded', (newComment) => {
      setComments([...comments, newComment]);
    });

    socket.on('commentUpdated', (updatedComment) => {
      setComments(
        comments.map((comment) =>
          comment.id === updatedComment.id ? updatedComment : comment
        )
      );
    });

    socket.on('commentDeleted', (deletedId) => {
      setComments(comments.filter((comment) => comment.id !== deletedId));
    });

    return () => {
      socket.disconnect();
    };
  }, [comments]);

  const handleAddComment = () => {
    if (newComment.trim()) {
      const newCommentObj: Comment = { id: Date.now(), text: newComment };
      setComments([...comments, newCommentObj]);
      setNewComment('');
      // Emit the comment to the server
      socket.emit('addComment', newCommentObj);
    }
  };

  const handleEditComment = (id: number) => {
    setEditingId(id);
  };

  const handleSaveEdit = (id: number, newText: string) => {
    if (newText.trim()) {
      const updatedComment: Comment = { id, text: newText };
      setComments(
        comments.map((comment) =>
          comment.id === id ? updatedComment : comment
        )
      );
      setEditingId(null);
      // Emit the updated comment to the server
      socket.emit('updateComment', updatedComment);
    }
  };

  const handleDeleteComment = (id: number) => {
    setComments(comments.filter((comment) => comment.id !== id));
    // Emit the deletion to the server
    socket.emit('deleteComment', id);
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-md max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Comments</h2>
      {editingId !== null ? (
        <div>
          <input
            type="text"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="border p-4 rounded-lg w-full mb-4 focus:outline-none focus:ring-2 ring-blue-500"
          />
          <button onClick={() => handleSaveEdit(editingId, newComment)} className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200">
            Save
          </button>
        </div>
      ) : (
        <>
          <input
            type="text"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="border p-4 rounded-lg w-full mb-6 focus:outline-none focus:ring-2 ring-blue-500"
          />
          <button onClick={handleAddComment} className="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors duration-200">
            Add Comment
          </button>
        </>
      )}
      {comments.map((comment) => (
        <div key={comment.id} className="mt-8 border-t border-gray-200 pt-4">
          <p>{comment.text}</p>
          <div className="flex space-x-4 mt-2">
            <button onClick={() => handleEditComment(comment.id)} className="text-blue-500 hover:text-blue-700 transition-colors duration-200">Edit</button>
            <button onClick={() => handleDeleteComment(comment.id)} className="text-red-500 hover:text-red-700 transition-colors duration-200">Delete</button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default CommentSection;
