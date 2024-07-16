// NDJSON Stream
declare module 'can-ndjson-stream' {
    export default function ndjsonStream(data: ReadableStream<Object>) : ReadableStream<Object>;
}