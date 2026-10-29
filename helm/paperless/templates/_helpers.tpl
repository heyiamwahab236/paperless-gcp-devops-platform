{{- define "paperless.name" -}}
{{- printf "%s-paperless" .Release.Name | trunc 45 | trimSuffix "-" -}}
{{- end -}}
{{- define "paperless.labels" -}}
app.kubernetes.io/name: paperless
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | quote }}
{{- end -}}
