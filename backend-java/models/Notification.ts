import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity()
export class Notification {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  eventType: string;

  @Column()
  userId: number;

  @CreateDateColumn({ type: 'timestamp' })
  timestamp: Date;

  @Column('text', { nullable: true })
  details?: string;
}
