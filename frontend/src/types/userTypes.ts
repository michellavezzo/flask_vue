export interface UserPreferences {
  timezone: string;
}

export interface User {
  username: string;
  password: string;
  roles: string[];
  preferences: UserPreferences;
  created_ts: number;
  active: boolean;
}
