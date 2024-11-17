import type { StateCreator, StoreApi } from 'zustand';
import type {
	StoreState,
	ChannelsState,
	ChannelsActions,
} from '../../types/index.ts';

interface ChannelsSliceState extends ChannelsState, ChannelsActions {}

export const createChannelsSlice: StateCreator<
	StoreState,
	[['zustand/devtools', never]],
	[],
	ChannelsSliceState
> = (set, _get, store: StoreApi<StoreState>) => ({
	currentChannel: null,

	createChannel: async (serverId, channelData) => {
		const response = await fetch(`/api/servers/${serverId}/channels`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': store.getState().csrfToken,
			},
			credentials: 'include',
			body: JSON.stringify(channelData),
		});

		if (response.ok) {
			const newChannel = await response.json();
			await store.getState().getServer(serverId);
			set({ currentChannel: newChannel }, false, 'channels/createChannel');
			return undefined;
		}

		const errorData = await response.json();
		return {
			server:
				errorData.errors?.message || 'Something went wrong. Please try again',
		};
	},

	updateChannel: async (channelId, updates) => {
		const response = await fetch(`/api/channels/${channelId}`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': store.getState().csrfToken,
			},
			credentials: 'include',
			body: JSON.stringify(updates),
		});

		if (response.ok) {
			const updatedChannel = await response.json();
			const currentServer = store.getState().currentServer;
			if (currentServer?.id) {
				await store.getState().getServer(currentServer.id);
			}

			set(
				(state) => ({
					currentChannel:
						state.currentChannel?.id === channelId
							? updatedChannel
							: state.currentChannel,
				}),
				false,
				'channels/updateChannel',
			);
			return undefined;
		}

		const errorData = await response.json();
		return {
			server:
				errorData.errors?.message || 'Something went wrong. Please try again',
		};
	},

	deleteChannel: async (channelId) => {
		const response = await fetch(`/api/channels/${channelId}`, {
			method: 'DELETE',
			headers: {
				'X-CSRFToken': store.getState().csrfToken,
			},
			credentials: 'include',
		});

		if (response.ok) {
			const currentServer = store.getState().currentServer;
			if (currentServer?.id) {
				await store.getState().getServer(currentServer.id);
			}

			set(
				(state) => ({
					currentChannel:
						state.currentChannel?.id === channelId
							? null
							: state.currentChannel,
				}),
				false,
				'channels/deleteChannel',
			);
			return undefined;
		}

		const errorData = await response.json();
		return {
			server:
				errorData.errors?.message || 'Something went wrong. Please try again',
		};
	},

	setCurrentChannel: (channel) => {
		set({ currentChannel: channel }, false, 'channels/setCurrentChannel');
	},
});

/*
Example of how to use this state slice:

Access channels from current server:

const channels = useStore(state => state.currentServer?.channels ?? []);

Access/modify current channel:

const currentChannel = useStore(state => state.currentChannel);
const setCurrentChannel = useStore(state => state.setCurrentChannel);



*/
