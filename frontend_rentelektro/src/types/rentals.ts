export type Rental = {
  id: number;
  tool_id: number;
  user_id: number;
  start_date: string;
  end_date: string;
  comment: string | null;
  owner_comment: string | null;
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
  tool_id: number;
  user_id: number;
  start_date: string;
  end_date: string;
  comment: string;
};
