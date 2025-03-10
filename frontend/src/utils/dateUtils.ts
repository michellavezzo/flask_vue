import { format, toZonedTime } from "date-fns-tz";

export const formatTimestamp = (timestamp: number, timezone?: string) => {
    const clientTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const selectedTimezone = timezone || clientTimezone;
    const date = toZonedTime(new Date(timestamp * 1000), selectedTimezone);
    return format(date, "EE, d/MM/yyyy | HH:mm:ss | 'GMT'XXX");
};
