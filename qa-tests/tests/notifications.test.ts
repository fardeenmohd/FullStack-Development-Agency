import { NotificationService } from '../src/services/NotificationService';
import { User } from '../src/models/User';

describe('NotificationService', () => {
  let notificationService: NotificationService;
  let mockUser: User;

  beforeEach(() => {
    notificationService = new NotificationService();
    mockUser = new User('123', 'John Doe');
  });

  describe('subscribeToNotifications', () => {
    it('should add user to the notification list', async () => {
      await notificationService.subscribeToNotifications(mockUser);
      expect(notificationService.notificationList).toContainEqual(mockUser);
    });

    it('should not add duplicate users', async () => {
      await notificationService.subscribeToNotifications(mockUser);
      await notificationService.subscribeToNotifications(mockUser);
      expect(notificationService.notificationList.length).toBe(1);
    });
  });

  describe('receiveNotification', () => {
    it('should send a notification to the user', async () => {
      const mockMessage = 'Hello, this is a test notification!';
      await notificationService.receiveNotification(mockUser, mockMessage);
      expect(notificationService.sentNotifications).toContainEqual({
        user: mockUser,
        message: mockMessage
      });
    });

    it('should handle errors when sending notifications', async () => {
      const mockError = new Error('Failed to send notification');
      jest.spyOn(notificationService, 'sendNotification').mockRejectedValue(mockError);
      await expect(notificationService.receiveNotification(mockUser, 'Test message')).rejects.toThrow(mockError);
    });
  });

  describe('handleErrors', () => {
    it('should log errors and continue processing', async () => {
      const mockError = new Error('An error occurred');
      jest.spyOn(console, 'error').mockImplementation(() => {});
      await notificationService.handleErrors(mockError);
      expect(console.error).toHaveBeenCalledWith(mockError);
    });
  });
});
