import { useEffect, useState } from "react";

type AsyncGeneratorHookReturnType<T> = {
    data?: T;
    loading: boolean;
    error?: Error;
    refetch: () => void;
}

export function useAsyncGenerator<T>(generatorFn:() => IterableIterator<Promise<T>>): AsyncGeneratorHookReturnType<T> {
    
    // Initial state
    const [state, setState] = useState<AsyncGeneratorHookReturnType<T>>({
        loading: true,
        refetch: () => {}
    });

    useEffect(() => {
        async function executeRequest(generator: IterableIterator<Promise<T>>) {
            try {
                const { value, done } = await generator.next();
                if(!done) {
                    setState((prevState) => ({
                        ...prevState,
                        data: value as any,
                        loading: false
                    }));
                    executeRequest(generator);
                } else {
                    setState((prevState) => ({
                        ...prevState,
                        loading: false,
                        data: value as any
                    }));
                }
            } catch (error) {
                setState((prevState) => ({
                    ...prevState,
                    loading: false,
                    error: error as Error
                }));
            }
        }

        function refetch() {
            setState((prevState) => ({
                ...prevState,
                loading: true
            }));
            executeRequest(generatorFn());
        }

        executeRequest(generatorFn());
        setState((prevState) => ({
            ...prevState,
            refetch
        }));
    }, []);

    return state;
};

