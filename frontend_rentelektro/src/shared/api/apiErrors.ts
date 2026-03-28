export type ApiErrorPayload = {
  detail?: string;
};

export class ApiClientError extends Error {
  status: number;
  payload?: ApiErrorPayload | string;

  constructor(message: string, status: number, payload?: ApiErrorPayload | string) {
    super(message);
    this.name = 'ApiClientError';
    this.status = status;
    this.payload = payload;
  }
}

const isApiErrorPayload = (value: unknown): value is ApiErrorPayload =>
  typeof value === 'object' && value !== null && 'detail' in value;

export const getApiErrorMessage = (error: unknown, fallbackMessage: string): string => {
  if (error instanceof ApiClientError) {
    if (typeof error.payload === 'string' && error.payload) {
      return error.payload;
    }

    if (isApiErrorPayload(error.payload) && error.payload.detail) {
      return error.payload.detail;
    }

    if (error.message) {
      return error.message;
    }
  }

  if (error instanceof Error && error.message) {
    return error.message;
  }

  return fallbackMessage;
};

type ApiResponse<T> = {
  data?: T;
  error?: unknown;
  response: Response;
};

export const assertApiResponse = (
  response: ApiResponse<unknown>,
  fallbackMessage: string,
): void => {
  if (response.error) {
    throw new ApiClientError(fallbackMessage, response.response.status, response.error as ApiErrorPayload | string);
  }
};

export const unwrapApiResponse = <T>(
  response: {
    data?: T;
    error?: unknown;
    response: Response;
  },
  fallbackMessage: string,
): T => {
  assertApiResponse(response, fallbackMessage);

  if (typeof response.data === 'undefined') {
    throw new ApiClientError(fallbackMessage, response.response.status);
  }

  return response.data;
};
