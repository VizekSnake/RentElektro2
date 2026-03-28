export type UserProfile = {
  id: number;
  email: string;
  lastname: string;
  phone: string;
  profile_picture: string;
  is_active: boolean;
  username: string;
  firstname: string;
  company: boolean;
  role: string | null;
};

export type UserProfileUpdate = Partial<
  Pick<
    UserProfile,
    'profile_picture' | 'username' | 'email' | 'phone' | 'firstname' | 'lastname' | 'company'
  >
>;

export type PasswordChangePayload = {
  current_password: string;
  new_password: string;
};

export type AccountAnonymizePayload = {
  current_password: string;
};
