// By Sam Herbert (@sherb), for everyone. More @ http://goo.gl/7AJzbL
export const svgRingsSpinner: string = String.raw`
<svg viewBox="0 0 45 45" xmlns="http://www.w3.org/2000/svg" stroke="currentColor">
    <g fill="none" fill-rule="evenodd" transform="translate(1 1)" stroke-width="2">
        <circle cx="22" cy="22" r="6" stroke-opacity="0">
            <animate attributeName="r"
                 begin="1.5s" dur="3s"
                 values="6;22"
                 calcMode="linear"
                 repeatCount="indefinite" />
            <animate attributeName="stroke-opacity"
                 begin="1.5s" dur="3s"
                 values="1;0" calcMode="linear"
                 repeatCount="indefinite" />
            <animate attributeName="stroke-width"
                 begin="1.5s" dur="3s"
                 values="2;0" calcMode="linear"
                 repeatCount="indefinite" />
        </circle>
        <circle cx="22" cy="22" r="6" stroke-opacity="0">
            <animate attributeName="r"
                 begin="3s" dur="3s"
                 values="6;22"
                 calcMode="linear"
                 repeatCount="indefinite" />
            <animate attributeName="stroke-opacity"
                 begin="3s" dur="3s"
                 values="1;0" calcMode="linear"
                 repeatCount="indefinite" />
            <animate attributeName="stroke-width"
                 begin="3s" dur="3s"
                 values="2;0" calcMode="linear"
                 repeatCount="indefinite" />
        </circle>
        <circle cx="22" cy="22" r="8">
            <animate attributeName="r"
                 begin="0s" dur="1.5s"
                 values="6;1;2;3;4;5;6"
                 calcMode="linear"
                 repeatCount="indefinite" />
        </circle>
    </g>
</svg>`

export const svgPuffSpinner: string = String.raw`
<svg viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg" stroke="currentColor">
    <g fill="none" fill-rule="evenodd" stroke-width="2">
        <circle cx="22" cy="22" r="1">
            <animate attributeName="r"
                begin="0s" dur="1.8s"
                values="1; 20"
                calcMode="spline"
                keyTimes="0; 1"
                keySplines="0.165, 0.84, 0.44, 1"
                repeatCount="indefinite" />
            <animate attributeName="stroke-opacity"
                begin="0s" dur="1.8s"
                values="1; 0"
                calcMode="spline"
                keyTimes="0; 1"
                keySplines="0.3, 0.61, 0.355, 1"
                repeatCount="indefinite" />
        </circle>
        <circle cx="22" cy="22" r="1">
            <animate attributeName="r"
                begin="-0.9s" dur="1.8s"
                values="1; 20"
                calcMode="spline"
                keyTimes="0; 1"
                keySplines="0.165, 0.84, 0.44, 1"
                repeatCount="indefinite" />
            <animate attributeName="stroke-opacity"
                begin="-0.9s" dur="1.8s"
                values="1; 0"
                calcMode="spline"
                keyTimes="0; 1"
                keySplines="0.3, 0.61, 0.355, 1"
                repeatCount="indefinite" />
        </circle>
    </g>
</svg>`

export const svgGridSpinner: string = String.raw`
<svg viewBox="0 0 105 105" xmlns="http://www.w3.org/2000/svg" fill="currentColor">
<circle cx="12.5" cy="12.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="0s" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="12.5" cy="52.5" r="12.5" fill-opacity=".5">
    <animate attributeName="fill-opacity"
     begin="100ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="52.5" cy="12.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="300ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="52.5" cy="52.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="600ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="92.5" cy="12.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="800ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="92.5" cy="52.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="400ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="12.5" cy="92.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="700ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="52.5" cy="92.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="500ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
<circle cx="92.5" cy="92.5" r="12.5">
    <animate attributeName="fill-opacity"
     begin="200ms" dur="1s"
     values="1;.2;1" calcMode="linear"
     repeatCount="indefinite" />
</circle>
</svg>`
