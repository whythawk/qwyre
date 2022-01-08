import { IWorkStateType, IMimeType, IContributorRoleType } from "./schema_types"
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IUserOpenProfileCreate,
} from "./profile"
import {
  IDataSource,
  IWork,
  IWorkMetadata,
  IWorkContents,
  IContributorMetadata,
  IOpinion,
  IWorkMetadataLineSummary,
  IWorkSearchSummary,
  IWorkLineSummary,
  IWorkMetadataSummary,
  IWorkSummary,
} from "./works"
import { ISubject } from "./subject"
import {
  ICoilUserResourceRequest,
  ICoilUserResourceResponse,
  ICoilUserTokenRequest,
  ICoilUserTokenResponse,
  ICoilUserTokenRefreshRequest,
  ICoilUserTokenRevokeRequest,
  ICoilUserInfo,
  ICoilUserBTP,
  ICoilMonetizationProgress,
} from "./coil"
import {
  IAnthology,
  ISeries,
  IConversion,
  IStream,
  IStreamIn,
  ILibrary,
} from "./collections"
import { ICurrencyTypes, IStripeIntent } from "./paystripe"
import {
  ISocketDataStream,
  ISocketResponse,
  ISendEmail,
  IMsg,
} from "./utilities"
import {
  ICreatorSummary,
  ICreatorProfile,
  IContributorSummary,
  ICreatorMini,
} from "./creator"
import {
  IPartyCreate,
  IPartyUpdate,
  IParty,
  IContractCreate,
  IContractUpdate,
  IContract,
} from "./contract"
import { IPageTheme, IPageSpacing, IPageFont, IThemeState } from "./theme"

// https://stackoverflow.com/a/64782482/295606
interface IKeyable {
  [key: string]: any | any[]
}

export {
  IKeyable,
  IWorkStateType,
  IMimeType,
  IContributorRoleType,
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IUserOpenProfileCreate,
  IDataSource,
  IWork,
  IWorkMetadata,
  IWorkContents,
  IContributorMetadata,
  IOpinion,
  IWorkMetadataLineSummary,
  IWorkSearchSummary,
  IWorkLineSummary,
  IWorkMetadataSummary,
  IWorkSummary,
  ISubject,
  ICoilUserResourceRequest,
  ICoilUserResourceResponse,
  ICoilUserTokenRequest,
  ICoilUserTokenResponse,
  ICoilUserTokenRefreshRequest,
  ICoilUserTokenRevokeRequest,
  ICoilUserInfo,
  IAnthology,
  ISeries,
  IConversion,
  IStream,
  IStreamIn,
  ILibrary,
  ICurrencyTypes,
  IStripeIntent,
  ICoilUserBTP,
  ICoilMonetizationProgress,
  ISocketDataStream,
  ISocketResponse,
  ISendEmail,
  IMsg,
  ICreatorSummary,
  ICreatorProfile,
  ICreatorMini,
  IContributorSummary,
  IPartyCreate,
  IPartyUpdate,
  IParty,
  IContractCreate,
  IContractUpdate,
  IContract,
  IPageTheme,
  IPageSpacing,
  IPageFont,
  IThemeState,
}
