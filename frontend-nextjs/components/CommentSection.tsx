"use client";
import React, { useState } from 'react';

interface Comment {
  id: number;
  text: string;
}

const CommentSection: React.FC<{ initialComments: Comment[] }> = ({ initialComments }) => {
  const [comments, setComments] = useState<Comment[]>(initialComments);
  const [newComment, setNewComment] = useState<string>('');
  const [editingId, setEditingId] = useState<number | null>(null);

  const handleAddComment = () => {
    if (newComment.trim()) {
      setComments([...comments, { id: Date.now(), text: newComment }]);
      setNewComment('');
    }
  };

  const handleEditComment = (id: number) => {
    setEditingId(id);
  };

  const handleSaveEdit = (id: number, newText: string) => {
    if (newText.trim()) {
      setComments(
        comments.map((comment) =>
          comment.id === id ? { ...comment, text: newText } : comment
        )
      );
      setEditingId(null);
    }
  };

  const handleDeleteComment = (id: number) => {
    setComments(comments.filter((comment) => comment.id !== id));
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4">Comments</h2>
      {editingId !== null ? (
        <div>
          <input
            type="text"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="border p-2 rounded-md w-full mb-2"
          />
          <button onClick={() => handleSaveEdit(editingId, newComment)}>
            Save
          </button>
        </div>
      ) : (
        <>
          <input
            type="text"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="border p-2 rounded-md w-full mb-4"
          />
          <button onClick={handleAddComment}>Add Comment</button>
        </>
      )}
      {comments.map((comment) => (
        <div key={comment.id} className="mt-4">
          <p>{comment.text}</p>
          <button onClick={() => handleEditComment(comment.id)}>Edit</button>
          <button onClick={() => handleDeleteComment(comment.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
};

export default CommentSection;
