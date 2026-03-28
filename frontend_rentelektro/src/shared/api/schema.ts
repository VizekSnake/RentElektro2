import type { UserProfile, UserProfileUpdate } from '@/types/profile';
import type {
  Rental,
  RentalCreatePayload,
  RentalDecisionPayload,
  RentalInboxItem,
  RentalNotificationsReadPayload,
  RentalNotificationsReadResult,
  RentalOwnerStatusPayload,
  RentalPaymentPayload,
} from '@/types/rentals';
import type { AccountAnonymizePayload, PasswordChangePayload } from '@/types/profile';
import type { PaginatedTools, Tool, ToolCategory, ToolFormPayload, ToolUpdatePayload } from '@/types/tools';

type ApiErrorPayload = {
  detail?: string;
};

type SessionUser = {
  id: number;
  username: string;
};

type LoginResult = {
  authenticated: boolean;
  token_type: string;
};

type SignUpPayload = {
  username: string;
  email: string;
  phone: string;
  firstname: string;
  lastname: string;
  company: boolean;
  password: string;
};

type RefreshTokenRequest = {
  refresh_token: string;
};

type RefreshTokenResponse = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};

export interface paths {
  '/users/token': {
    post: {
      requestBody: {
        content: {
          'application/x-www-form-urlencoded': {
            username: string;
            password: string;
          };
        };
      };
      responses: {
        200: {
          content: {
            'application/json': LoginResult;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/users/me': {
    get: {
      responses: {
        200: {
          content: {
            'application/json': SessionUser;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/users/refresh': {
    post: {
      requestBody?: {
        content: {
          'application/json': RefreshTokenRequest;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': RefreshTokenResponse;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/users/logout': {
    post: {
      responses: {
        204: {
          content: never;
        };
      };
    };
  };
  '/users/register': {
    post: {
      requestBody: {
        content: {
          'application/json': SignUpPayload;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': unknown;
          };
        };
        422: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/users/me/data': {
    get: {
      responses: {
        200: {
          content: {
            'application/json': UserProfile;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/users/user/{user_id}': {
    patch: {
      parameters: {
        path: {
          user_id: number;
        };
      };
      requestBody: {
        content: {
          'application/json': UserProfileUpdate;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': unknown;
          };
        };
        422: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/users/me/password': {
    post: {
      requestBody: {
        content: {
          'application/json': PasswordChangePayload;
        };
      };
      responses: {
        204: {
          content: never;
        };
        400: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/users/me/anonymize': {
    post: {
      requestBody: {
        content: {
          'application/json': AccountAnonymizePayload;
        };
      };
      responses: {
        204: {
          content: never;
        };
        400: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/tool/all': {
    get: {
      parameters?: {
        query?: {
          search?: string;
          power_source?: string;
          availability?: boolean;
          category_id?: number;
          sort?: 'newest' | 'price_asc' | 'price_desc' | 'name';
          page?: number;
          page_size?: number;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': PaginatedTools;
          };
        };
      };
    };
  };
  '/tool/{tool_id}': {
    get: {
      parameters: {
        path: {
          tool_id: number;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': Tool;
          };
        };
        404: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/tool/category/all': {
    get: {
      responses: {
        200: {
          content: {
            'application/json': ToolCategory[] | null;
          };
        };
      };
    };
  };
  '/tool/mine': {
    get: {
      responses: {
        200: {
          content: {
            'application/json': Tool[];
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/tool/add': {
    post: {
      requestBody: {
        content: {
          'application/json': ToolFormPayload;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': Tool;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
        422: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/tool/update/{tool_id}': {
    patch: {
      parameters: {
        path: {
          tool_id: number;
        };
      };
      requestBody: {
        content: {
          'application/json': ToolUpdatePayload;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': Tool;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
        422: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/rental/add': {
    post: {
      requestBody: {
        content: {
          'application/json': RentalCreatePayload;
        };
      };
      responses: {
        201: {
          content: {
            'application/json': Rental;
          };
        };
        422: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/rental/inbox': {
    get: {
      responses: {
        200: {
          content: {
            'application/json': RentalInboxItem[];
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/rental/my': {
    get: {
      responses: {
        200: {
          content: {
            'application/json': RentalInboxItem[];
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/rental/notifications/read': {
    patch: {
      requestBody: {
        content: {
          'application/json': RentalNotificationsReadPayload;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': RentalNotificationsReadResult;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/rental/{rental_id}/decision': {
    patch: {
      parameters: {
        path: {
          rental_id: number;
        };
      };
      requestBody: {
        content: {
          'application/json': RentalDecisionPayload;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': Rental;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/rental/{rental_id}/pay': {
    patch: {
      parameters: {
        path: {
          rental_id: number;
        };
      };
      requestBody: {
        content: {
          'application/json': RentalPaymentPayload;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': Rental;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
  '/rental/{rental_id}/owner-status': {
    patch: {
      parameters: {
        path: {
          rental_id: number;
        };
      };
      requestBody: {
        content: {
          'application/json': RentalOwnerStatusPayload;
        };
      };
      responses: {
        200: {
          content: {
            'application/json': Rental;
          };
        };
        401: {
          content: {
            'application/json': ApiErrorPayload;
          };
        };
      };
    };
  };
}
