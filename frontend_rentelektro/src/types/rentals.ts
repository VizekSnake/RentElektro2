import type { components } from '@/shared/api/generated/schema';

export type Rental = components['schemas']['Rental'];
export type RentalCreatePayload = components['schemas']['RentalAdd'];
export type RentalInboxItem = components['schemas']['RentalInboxItem'];
export type RentalDecisionPayload = components['schemas']['RentalDecisionUpdate'];
export type RentalPaymentPayload = components['schemas']['RentalPaymentUpdate'];
export type RentalOwnerStatusPayload = components['schemas']['RentalOwnerStatusUpdate'];
export type RentalNotificationsReadPayload = components['schemas']['RentalNotificationsReadUpdate'];
export type RentalNotificationsReadResult = components['schemas']['RentalNotificationsReadResult'];
