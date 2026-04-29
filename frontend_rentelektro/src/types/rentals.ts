import type { UUID } from '@/types/identifiers';

export type Rental = {
  id: UUID;
  tool_id: UUID;
  user_id: UUID;
  start_date: string;
  end_date: string;
  comment: string | null;
  owner_comment: string | null;
  is_paid: boolean;
  paid_at: string | null;
  handed_over_at: string | null;
  returned_at: string | null;
  renter_seen_at: string | null;
  status:
    | 'accepted'
    | 'rejected_by_owner'
    | 'canceled'
    | 'fulfilled'
    | 'paid_rented'
    | 'paid_not_rented'
    | 'viewed'
    | 'not_viewed'
    | 'problem'
    | 'scam';
};

export type RentalCreatePayload = {
  tool_id: UUID;
  user_id: UUID;
  start_date: string;
  end_date: string;
  comment: string;
};

export type RentalInboxItem = Rental & {
  tool: {
    id: UUID;
    Type: string;
    TypeLabel?: string | null;
    Brand: string;
    PowerSourceLabel?: string | null;
    ImageURL: string | null;
    RatePerDay: number | null;
  };
  requester: {
    id: UUID;
    username: string;
    firstname: string;
    lastname: string;
    email: string;
    phone: string | null;
  };
  owner: {
    id: UUID;
    username: string;
    firstname: string;
    lastname: string;
    email: string;
    phone: string | null;
  };
};

export type RentalDecisionPayload = {
  status: 'accepted' | 'rejected_by_owner';
  owner_comment?: string;
};

export type RentalPaymentPayload = {
  cardholder: string;
  card_number: string;
  expiry_date: string;
  cvc: string;
};

export type RentalOwnerStatusPayload = {
  status: 'paid_rented' | 'fulfilled';
};

export type RentalNotificationsReadPayload = {
  scope: 'owner' | 'renter' | 'all';
};

export type RentalNotificationsReadResult = {
  scope: 'owner' | 'renter' | 'all';
  updated_owner: number;
  updated_renter: number;
};
