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
