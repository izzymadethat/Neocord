import type React from 'react';
import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useStore } from '../../store/store.ts';

function SignupFormPage() {
	const navigate = useNavigate();
	const signup = useStore((state) => state.signup);
	const user = useStore((state) => state.user);
	const [email, setEmail] = useState('');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [errors, setErrors] = useState<Record<string, string>>({});

	if (user) return <Navigate to='/' replace={true} />;

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();

		if (password !== confirmPassword) {
			return setErrors({
				confirmPassword:
					'Confirm Password field must be the same as the Password field',
			});
		}

		const serverResponse = await signup({
			email,
			username,
			password,
		});

		if (serverResponse) {
			setErrors(serverResponse);
		} else {
			navigate('/');
		}
	};

	return (
		<>
			<h1>Sign Up</h1>
			{errors.server && <p>{errors.server}</p>}
			<form onSubmit={handleSubmit}>
				<label>
					Email
					<input
						type='text'
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						required={true}
					/>
				</label>
				{errors.email && <p>{errors.email}</p>}
				<label>
					Username
					<input
						type='text'
						value={username}
						onChange={(e) => setUsername(e.target.value)}
						required={true}
					/>
				</label>
				{errors.username && <p>{errors.username}</p>}
				<label>
					Password
					<input
						type='password'
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required={true}
					/>
				</label>
				{errors.password && <p>{errors.password}</p>}
				<label>
					Confirm Password
					<input
						type='password'
						value={confirmPassword}
						onChange={(e) => setConfirmPassword(e.target.value)}
						required={true}
					/>
				</label>
				{errors.confirmPassword && <p>{errors.confirmPassword}</p>}
				<button type='submit'>Sign Up</button>
			</form>
		</>
	);
}

export { SignupFormPage };
