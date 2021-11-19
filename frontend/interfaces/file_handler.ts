// The following typings implement the relevant parts of the File System Access
// API. This can be removed once the specification reaches the Candidate phase
// and is implemented as part of microsoft/TSJS-lib-generator.

// https://github.com/GoogleChromeLabs/browser-fs-access/blob/a0c85840572a14ca29b1d9984a8e4e52524ca688/index.d.ts
// Not reachable from the source.

export interface FileSystemHandlePermissionDescriptor {
  mode?: "read" | "readwrite"
}

export interface FileSystemHandle {
  readonly kind: "file" | "directory"
  readonly name: string

  isSameEntry: (other: FileSystemHandle) => Promise<boolean>

  queryPermission: (
    descriptor?: FileSystemHandlePermissionDescriptor
  ) => Promise<PermissionState>
  requestPermission: (
    descriptor?: FileSystemHandlePermissionDescriptor
  ) => Promise<PermissionState>
}

export interface FileWithHandle extends File {
  handle?: FileSystemHandle
}
