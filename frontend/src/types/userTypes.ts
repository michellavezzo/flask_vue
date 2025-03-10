export interface UserPreferences {
    timezone: string;
}
export interface User {
    username: string;
    password: string;
    roles: string[];
    preferences: UserPreferences;
    last_updated_at?: number;
    created_ts: number;
    active: boolean;
}
